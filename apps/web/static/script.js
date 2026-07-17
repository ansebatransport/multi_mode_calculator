/* ===== STATE ===== */
let currentMode = 'standard';
let history = [];

/* Standard/Scientific state */
let expression = '';
let result = '0';
let newNumber = true;
let lastWasEquals = false;

/* Programmer state */
let progValue = 0;
let progInput = '0';
let progNewNumber = true;
let progBase = 10;
let progPendingOp = null;
let progFirstOperand = 0;

/* Angle mode for scientific */
let angleMode = 'DEG';

/* ===== DOM REFS ===== */
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

/* ===== MODE SWITCHING ===== */
function switchMode(mode) {
    currentMode = mode;
    $$('.page').forEach(p => p.classList.remove('active'));
    $(`#page-${mode}`).classList.add('active');
    $('#mode-label').textContent = {
        standard: 'Standard', scientific: 'Scientific', programmer: 'Programmer',
        graph: 'Graph', converter: 'Unit Converter', financial: 'Financial'
    }[mode];
    $$('.menu-item').forEach(item => {
        item.classList.toggle('active', item.dataset.mode === mode);
    });
    closeMenu();
    if (mode === 'graph') setTimeout(plotGraph, 100);
    if (mode === 'converter') initConverter();
}

/* ===== HAMBURGER MENU ===== */
function toggleMenu() {
    $('#hamburger-menu').classList.toggle('open');
}

function closeMenu() {
    $('#hamburger-menu').classList.remove('open');
}

$('#hamburger-btn').addEventListener('click', toggleMenu);

$$('.menu-item').forEach(item => {
    item.addEventListener('click', () => switchMode(item.dataset.mode));
});

document.addEventListener('click', (e) => {
    if (!e.target.closest('.hamburger-menu') && !e.target.closest('.hamburger-btn')) {
        closeMenu();
    }
});

/* ===== HISTORY ===== */
function addHistory(expr, res) {
    history.unshift({ expression: expr, result: res });
    if (history.length > 50) history.pop();
    renderHistory();
}

function renderHistory() {
    const list = $('#history-list');
    if (history.length === 0) {
        list.innerHTML = '<div class="history-empty">No history yet</div>';
        return;
    }
    list.innerHTML = history.map((h, i) => `
        <div class="history-item" data-idx="${i}">
            <div class="history-expr">${h.expression}</div>
            <div class="history-result">${h.result}</div>
        </div>
    `).join('');
    list.querySelectorAll('.history-item').forEach(item => {
        item.addEventListener('click', () => {
            const entry = history[item.dataset.idx];
            result = entry.result;
            newNumber = true;
            updateStdDisplay();
            $('#history-panel').classList.remove('open');
        });
    });
}

$('#btn-history').addEventListener('click', () => {
    $('#history-panel').classList.toggle('open');
    renderHistory();
});

$('#history-close').addEventListener('click', () => {
    $('#history-panel').classList.remove('open');
});

/* ===== THEME (no-op, dark only for now) ===== */
$('#btn-theme').addEventListener('click', () => {});
$('#btn-minimize').addEventListener('click', () => {});
$('#btn-maximize').addEventListener('click', () => {});
$('#btn-close').addEventListener('click', () => {});

/* ======================================================
   STANDARD MODE
   ====================================================== */
function updateStdDisplay() {
    $('#std-expression').textContent = expression;
    $('#std-result').textContent = result;
}

function stdAction(action) {
    switch (action) {
        case 'clear':
            expression = '';
            result = '0';
            newNumber = true;
            lastWasEquals = false;
            break;
        case 'ce':
            result = '0';
            newNumber = true;
            break;
        case 'backspace':
            if (result.length > 1) result = result.slice(0, -1);
            else result = '0';
            break;
        case 'negate':
            if (result !== '0' && result !== 'Error') {
                result = result.startsWith('-') ? result.slice(1) : '-' + result;
            }
            break;
        case 'percent':
            if (expression) {
                const base = parseFloat(calculateLocal(expression.replace(/[+\-*/]$/, '')));
                result = String(base * parseFloat(result) / 100);
            } else {
                result = String(parseFloat(result) / 100);
            }
            newNumber = true;
            break;
        case 'reciprocal':
            if (parseFloat(result) === 0) { result = 'Error'; }
            else { result = String(1 / parseFloat(result)); }
            newNumber = true;
            break;
        case 'square':
            result = String(Math.pow(parseFloat(result), 2));
            newNumber = true;
            break;
        case 'sqrt':
            result = String(Math.sqrt(parseFloat(result)));
            newNumber = true;
            break;
        case 'calculate':
            calculateStd();
            return;
    }
    updateStdDisplay();
}

function calculateStd() {
    if (!expression) return;
    const fullExpr = expression + result;
    sendCalculate(fullExpr, (res) => {
        addHistory(fullExpr, res);
        expression = '';
        result = res;
        newNumber = true;
        lastWasEquals = true;
        updateStdDisplay();
    });
}

/* ======================================================
   SCIENTIFIC MODE
   ====================================================== */
function updateSciDisplay() {
    $('#sci-expression').textContent = expression;
    $('#sci-result').textContent = result;
    $('#angle-mode').textContent = angleMode;
    $$('.sci')[0].textContent = angleMode;
}

function sciAction(action) {
    if (action === 'angle-toggle') {
        const modes = ['DEG', 'RAD', 'GRAD'];
        angleMode = modes[(modes.indexOf(angleMode) + 1) % 3];
        updateSciDisplay();
        return;
    }
    if (action === 'clear') { stdAction('clear'); updateSciDisplay(); return; }
    if (action === 'backspace') { stdAction('backspace'); updateSciDisplay(); return; }
    if (action === 'negate') { stdAction('negate'); updateSciDisplay(); return; }
    if (action === 'percent') { stdAction('percent'); updateSciDisplay(); return; }
    if (action === 'reciprocal') { stdAction('reciprocal'); updateSciDisplay(); return; }
    if (action === 'square') { stdAction('square'); updateSciDisplay(); return; }
    if (action === 'sqrt') { stdAction('sqrt'); updateSciDisplay(); return; }
    if (action === 'calculate') { calculateStd(); updateSciDisplay(); return; }

    const funcs = {
        sin: 'sin', cos: 'cos', tan: 'tan',
        asin: 'asin', acos: 'acos', atan: 'atan',
        sinh: 'sinh', cosh: 'cosh', tanh: 'tanh',
        asinh: 'asinh', acosh: 'acosh', atanh: 'atanh',
        ln: 'ln', log10: 'log', cbrt: 'cbrt',
        factorial: 'factorial',
    };

    if (funcs[action]) {
        if (newNumber) {
            expression += funcs[action] + '(';
        } else {
            expression += funcs[action] + '(' + result + ')';
        }
        newNumber = true;
        updateSciDisplay();
        return;
    }

    if (action === 'pi') {
        result = String(Math.PI);
        newNumber = true;
        updateSciDisplay();
        return;
    }
    if (action === 'euler') {
        result = String(Math.E);
        newNumber = true;
        updateSciDisplay();
        return;
    }
    if (action === 'power') {
        expression += result + '**';
        result = '0';
        newNumber = true;
        updateSciDisplay();
        return;
    }
    if (action === 'pow10') {
        expression += '10**(' + result + ')';
        newNumber = true;
        calculateSciExpr();
        return;
    }
    if (action === 'expx') {
        expression += 'exp(' + result + ')';
        newNumber = true;
        calculateSciExpr();
        return;
    }
    if (action === 'mod') {
        expression += result + '%';
        result = '0';
        newNumber = true;
        updateSciDisplay();
        return;
    }
}

function calculateSciExpr() {
    sendCalculate(expression, (res) => {
        addHistory(expression, res);
        expression = '';
        result = res;
        newNumber = true;
        lastWasEquals = true;
        updateSciDisplay();
    });
}

/* ======================================================
   API CALL
   ====================================================== */
async function sendCalculate(expr, callback) {
    try {
        const resp = await fetch('/api/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression: expr })
        });
        const data = await resp.json();
        if (data.error) {
            callback('Error');
        } else {
            callback(formatNum(data.result));
        }
    } catch (e) {
        callback('Error');
    }
}

function formatNum(val) {
    if (typeof val === 'string') return val;
    if (Number.isInteger(val) && Math.abs(val) < 1e15) return String(val);
    if (Math.abs(val) > 1e15 || (Math.abs(val) < 1e-10 && val !== 0)) return val.toExponential(6);
    return parseFloat(val.toPrecision(12)).toString();
}

/* ======================================================
   PROGRAMMER MODE
   ====================================================== */
function updateProgDisplay() {
    $('#prog-result').textContent = progInput;
    try {
        const bases = progToAllBases(progValue);
        $('#prog-hex').textContent = '0x' + bases.hex;
        $('#prog-dec').textContent = bases.dec;
        $('#prog-oct').textContent = '0o' + bases.oct;
        $('#prog-bin').textContent = '0b' + bases.bin;
    } catch (e) {}
    $$('.hex-btn').forEach(b => {
        b.classList.toggle('disabled', progBase < 16);
    });
    $$('.base-btn').forEach(b => {
        b.classList.toggle('active', parseInt(b.dataset.base) === progBase);
    });
}

function progToAllBases(val) {
    const toBase = (v, b) => {
        if (v === 0) return '0';
        const neg = v < 0;
        v = Math.abs(v);
        const digits = '0123456789ABCDEF';
        let s = '';
        while (v > 0) { s = digits[v % b] + s; v = Math.floor(v / b); }
        return neg ? '-' + s : s;
    };
    return { hex: toBase(val, 16), dec: String(val), oct: toBase(val, 8), bin: toBase(val, 2) };
}

function progDigit(d) {
    const maxDigit = progBase <= 10 ? 9 : 15;
    const dVal = parseInt(d, 16);
    if (dVal >= progBase) return;
    if (progNewNumber) { progInput = d; progNewNumber = false; }
    else { progInput += d; }
    try { progValue = parseInt(progInput, progBase); } catch (e) {}
    updateProgDisplay();
}

function progOp(op) {
    progPendingOp = op;
    progFirstOperand = progValue;
    progNewNumber = true;
}

function progEquals() {
    if (!progPendingOp) return;
    const ops = {
        AND: (a, b) => a & b, OR: (a, b) => a | b, XOR: (a, b) => a ^ b,
        LSHIFT: (a, b) => a << b, RSHIFT: (a, b) => a >> b,
        '+': (a, b) => a + b, '-': (a, b) => a - b, '*': (a, b) => a * b,
    };
    if (ops[progPendingOp]) progValue = ops[progPendingOp](progFirstOperand, progValue);
    else if (progPendingOp === 'NOT') progValue = ~progFirstOperand;
    progInput = String(progValue);
    progPendingOp = null;
    progNewNumber = true;
    updateProgDisplay();
}

function progAction(action) {
    if (action === 'clear') { progValue = 0; progInput = '0'; progNewNumber = true; progPendingOp = null; updateProgDisplay(); return; }
    if (action === 'backspace') { progInput = progInput.length > 1 ? progInput.slice(0, -1) : '0'; try { progValue = parseInt(progInput, progBase); } catch(e) {} updateProgDisplay(); return; }
    if (action === 'negate') { progValue = -progValue; progInput = String(progValue); progNewNumber = true; updateProgDisplay(); return; }
    if (action === 'bitnot') { progValue = ~progValue; progInput = String(progValue); progNewNumber = true; updateProgDisplay(); return; }
    if (['bitand', 'bitor', 'bitxor', 'lshift', 'rshift'].includes(action)) {
        const opMap = { bitand: 'AND', bitor: 'OR', bitxor: 'XOR', lshift: 'LSHIFT', rshift: 'RSHIFT' };
        progOp(opMap[action]);
        return;
    }
    if (action === 'prog-equals') { progEquals(); return; }
}

/* ===== GRAPH MODE ===== */
function plotGraph() {
    const canvas = $('#graph-canvas');
    const ctx = canvas.getContext('2d');
    const w = canvas.width = canvas.offsetWidth * 2;
    const h = canvas.height = canvas.offsetHeight * 2;
    ctx.clearRect(0, 0, w, h);

    const xMin = parseFloat($('#x-min').value) || -10;
    const xMax = parseFloat($('#x-max').value) || 10;
    const yMin = parseFloat($('#y-min').value) || -10;
    const yMax = parseFloat($('#y-max').value) || 10;
    const fn = $('#graph-input').value || '0';

    const toX = (x) => (x - xMin) / (xMax - xMin) * w;
    const toY = (y) => h - (y - yMin) / (yMax - yMin) * h;

    /* Grid */
    ctx.strokeStyle = '#1a2a4a';
    ctx.lineWidth = 1;
    for (let x = Math.ceil(xMin); x <= xMax; x++) {
        ctx.beginPath(); ctx.moveTo(toX(x), 0); ctx.lineTo(toX(x), h); ctx.stroke();
    }
    for (let y = Math.ceil(yMin); y <= yMax; y++) {
        ctx.beginPath(); ctx.moveTo(0, toY(y)); ctx.lineTo(w, toY(y)); ctx.stroke();
    }

    /* Axes */
    ctx.strokeStyle = '#3a4a6a';
    ctx.lineWidth = 2;
    if (yMin <= 0 && yMax >= 0) {
        ctx.beginPath(); ctx.moveTo(0, toY(0)); ctx.lineTo(w, toY(0)); ctx.stroke();
    }
    if (xMin <= 0 && xMax >= 0) {
        ctx.beginPath(); ctx.moveTo(toX(0), 0); ctx.lineTo(toX(0), h); ctx.stroke();
    }

    /* Function */
    const mathFn = buildMathFn(fn);
    if (!mathFn) return;

    ctx.strokeStyle = '#e94560';
    ctx.lineWidth = 3;
    ctx.beginPath();
    let started = false;
    const steps = w;
    for (let i = 0; i <= steps; i++) {
        const x = xMin + (xMax - xMin) * i / steps;
        try {
            const y = mathFn(x);
            if (!isFinite(y) || Math.abs(y) > 1e6) { started = false; continue; }
            const px = toX(x);
            const py = toY(y);
            if (!started) { ctx.moveTo(px, py); started = true; }
            else { ctx.lineTo(px, py); }
        } catch (e) { started = false; }
    }
    ctx.stroke();
}

function buildMathFn(expr) {
    try {
        const sanitized = expr
            .replace(/\bsin\b/g, 'Math.sin')
            .replace(/\bcos\b/g, 'Math.cos')
            .replace(/\btan\b/g, 'Math.tan')
            .replace(/\basin\b/g, 'Math.asin')
            .replace(/\bacos\b/g, 'Math.acos')
            .replace(/\batan\b/g, 'Math.atan')
            .replace(/\bsinh\b/g, 'Math.sinh')
            .replace(/\bcosh\b/g, 'Math.cosh')
            .replace(/\btanh\b/g, 'Math.tanh')
            .replace(/\bsqrt\b/g, 'Math.sqrt')
            .replace(/\bcbrt\b/g, 'Math.cbrt')
            .replace(/\blog\b/g, 'Math.log10')
            .replace(/\bln\b/g, 'Math.log')
            .replace(/\bexp\b/g, 'Math.exp')
            .replace(/\babs\b/g, 'Math.abs')
            .replace(/\bpi\b/g, 'Math.PI')
            .replace(/\be\b(?![xp])/g, 'Math.E')
            .replace(/\^/g, '**');
        return new Function('x', `"use strict"; return (${sanitized});`);
    } catch (e) { return null; }
}

$('#plot-btn').addEventListener('click', plotGraph);
$$('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        $('#graph-input').value = btn.dataset.fn;
        plotGraph();
    });
});

/* ===== UNIT CONVERTER ===== */
let unitData = {};
let convFromUnits = [];
let convToUnits = [];

async function initConverter() {
    if (Object.keys(unitData).length === 0) {
        try {
            const resp = await fetch('/api/unit/categories');
            unitData = await resp.json();
        } catch (e) { return; }
    }
    const catSelect = $('#conv-category');
    if (catSelect.options.length === 0) {
        Object.keys(unitData).forEach(cat => {
            catSelect.add(new Option(cat, cat));
        });
        catSelect.addEventListener('change', updateConvUnits);
        $('#conv-from').addEventListener('change', doConvert);
        $('#conv-to').addEventListener('change', doConvert);
        $('#conv-from-val').addEventListener('input', doConvert);
        $('#conv-swap').addEventListener('click', swapConvUnits);
    }
    updateConvUnits();
}

function updateConvUnits() {
    const cat = $('#conv-category').value;
    const units = unitData[cat] || [];
    const fromSel = $('#conv-from');
    const toSel = $('#conv-to');
    fromSel.innerHTML = '';
    toSel.innerHTML = '';
    units.forEach((u, i) => {
        fromSel.add(new Option(`${u.name} (${u.symbol})`, u.name));
        toSel.add(new Option(`${u.name} (${u.symbol})`, u.name));
    });
    if (units.length > 1) toSel.selectedIndex = 1;
    doConvert();
}

async function doConvert() {
    const cat = $('#conv-category').value;
    const from = $('#conv-from').value;
    const to = $('#conv-to').value;
    const val = parseFloat($('#conv-from-val').value);
    if (isNaN(val)) { $('#conv-to-val').value = ''; return; }
    try {
        const resp = await fetch('/api/unit/convert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ value: val, from_unit: from, to_unit: to, category: cat })
        });
        const data = await resp.json();
        if (data.error) $('#conv-to-val').value = 'Error';
        else $('#conv-to-val').value = formatNum(data.result);
    } catch (e) { $('#conv-to-val').value = 'Error'; }
}

function swapConvUnits() {
    const fromSel = $('#conv-from');
    const toSel = $('#conv-to');
    const tmp = fromSel.value;
    fromSel.value = toSel.value;
    toSel.value = tmp;
    doConvert();
}

/* ===== FINANCIAL MODE ===== */
$$('.fin-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        $$('.fin-tab').forEach(t => t.classList.remove('active'));
        $$('.fin-panel').forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        $(`#fin-${tab.dataset.tab}`).classList.add('active');
    });
});

$$('.fin-sub-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const parent = tab.closest('.fin-panel');
        parent.querySelectorAll('.fin-sub-tab').forEach(t => t.classList.remove('active'));
        parent.querySelectorAll('.fin-sub-panel').forEach(p => p.classList.remove('active'));
        tab.classList.add('active');
        parent.querySelector(`#stab-${tab.dataset.stab}`).classList.add('active');
    });
});

$('#int-type').addEventListener('change', () => {
    $('#int-periods-field').style.display = $('#int-type').value === 'compound' ? 'block' : 'none';
});

async function api(path, data) {
    const resp = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
    return resp.json();
}

function showResult(id, html) {
    const el = $(id);
    el.classList.add('visible');
    el.innerHTML = html;
}

$('#tvm-solve').addEventListener('click', async () => {
    const data = {};
    ['n', 'i', 'pv', 'pmt', 'fv'].forEach(k => {
        const el = $(`#tvm-${k}`);
        if (el.value !== '') data[k] = parseFloat(el.value);
    });
    const result = await api('/api/financial/tvm', data);
    if (result.error) { showResult('#tvm-result', 'Error: ' + result.error); return; }
    let txt = '';
    if (result.n !== undefined) txt += `N = ${formatNum(result.n)}\n`;
    if (result.i_y !== undefined) txt += `I/Y = ${formatNum(result.i_y)}%\n`;
    if (result.pv !== undefined) txt += `PV = $${formatNum(result.pv)}\n`;
    if (result.pmt !== undefined) txt += `PMT = $${formatNum(result.pmt)}\n`;
    if (result.fv !== undefined) txt += `FV = $${formatNum(result.fv)}`;
    showResult('#tvm-result', txt);
});

$('#mort-calc').addEventListener('click', async () => {
    const r = await api('/api/financial/mortgage', {
        principal: parseFloat($('#mort-principal').value),
        annual_rate: parseFloat($('#mort-rate').value),
        years: parseInt($('#mort-years').value),
    });
    if (r.error) { showResult('#mort-result', 'Error: ' + r.error); return; }
    showResult('#mort-result', `Monthly Payment: $${formatNum(r.monthly_payment)}\nTotal Payment: $${formatNum(r.total_payment)}\nTotal Interest: $${formatNum(r.total_interest)}`);
});

$('#car-calc').addEventListener('click', async () => {
    const r = await api('/api/financial/car_loan', {
        principal: parseFloat($('#car-principal').value),
        annual_rate: parseFloat($('#car-rate').value),
        months: parseInt($('#car-months').value),
    });
    if (r.error) { showResult('#car-result', 'Error: ' + r.error); return; }
    showResult('#car-result', `Monthly Payment: $${formatNum(r.monthly_payment)}\nTotal Payment: $${formatNum(r.total_payment)}\nTotal Interest: $${formatNum(r.total_interest)}`);
});

$('#int-calc').addEventListener('click', async () => {
    const r = await api('/api/financial/interest', {
        principal: parseFloat($('#int-principal').value),
        rate: parseFloat($('#int-rate').value),
        time: parseFloat($('#int-time').value),
        mode: $('#int-type').value,
        periods: parseInt($('#int-periods').value) || 12,
    });
    if (r.error) { showResult('#int-result', 'Error: ' + r.error); return; }
    if (r.interest !== undefined && r.total !== undefined)
        showResult('#int-result', `Interest: $${formatNum(r.interest)}\nTotal: $${formatNum(r.total)}`);
    else
        showResult('#int-result', `Amount: $${formatNum(r.amount)}\nInterest: $${formatNum(r.interest)}`);
});

$('#npv-calc').addEventListener('click', async () => {
    const r = await api('/api/financial/npv', {
        rate: parseFloat($('#npv-rate').value),
        cashflows: $('#npv-cashflows').value.split(',').map(Number),
    });
    showResult('#npv-result', r.error ? 'Error: ' + r.error : `NPV = $${formatNum(r.result)}`);
});

$('#irr-calc').addEventListener('click', async () => {
    const r = await api('/api/financial/irr', {
        cashflows: $('#npv-cashflows').value.split(',').map(Number),
    });
    showResult('#npv-result', r.error ? 'Error: ' + r.error : `IRR = ${(r.result * 100).toFixed(4)}%`);
});

$('#mirr-calc').addEventListener('click', async () => {
    const r = await api('/api/financial/mirr', {
        cashflows: $('#npv-cashflows').value.split(',').map(Number),
        finance_rate: parseFloat($('#mirr-finance').value),
        reinvest_rate: parseFloat($('#mirr-reinvest').value),
    });
    showResult('#npv-result', r.error ? 'Error: ' + r.error : `MIRR = ${(r.result * 100).toFixed(4)}%`);
});

$('#dep-calc').addEventListener('click', async () => {
    const r = await api('/api/financial/depreciation', {
        cost: parseFloat($('#dep-cost').value),
        salvage: parseFloat($('#dep-salvage').value),
        life: parseInt($('#dep-life').value),
        method: $('#dep-method').value,
    });
    if (r.error) { showResult('#dep-result', 'Error: ' + r.error); return; }
    let html = '<table><tr><th>Year</th><th>Depreciation</th><th>Accumulated</th><th>Book Value</th></tr>';
    r.schedule.forEach(row => {
        html += `<tr><td>${row.year}</td><td>$${formatNum(row.depreciation)}</td><td>$${formatNum(row.accumulated)}</td><td>$${formatNum(row.book_value)}</td></tr>`;
    });
    html += '</table>';
    showResult('#dep-result', html);
});

$('#bond-calc').addEventListener('click', async () => {
    const r = await api('/api/financial/bond', {
        face: parseFloat($('#bond-face').value),
        coupon_rate: parseFloat($('#bond-coupon').value),
        ytm: parseFloat($('#bond-ytm').value),
        years: parseInt($('#bond-years').value),
        freq: parseInt($('#bond-freq').value),
    });
    if (r.error) { showResult('#bond-result', 'Error: ' + r.error); return; }
    showResult('#bond-result', `Bond Price: $${formatNum(r.dirty_price)}\nCurrent Yield: ${r.current_yield}%\nAnnual Coupon: $${formatNum(r.total_coupon)}`);
});

$('#be-calc').addEventListener('click', async () => {
    const r = await api('/api/financial/break_even', {
        fixed_costs: parseFloat($('#be-fixed').value),
        price_per_unit: parseFloat($('#be-price').value),
        variable_cost_per_unit: parseFloat($('#be-variable').value),
    });
    if (r.error) { showResult('#be-result', 'Error: ' + r.error); return; }
    showResult('#be-result', `Break-Even Units: ${r.break_even_units}\nBreak-Even Revenue: $${formatNum(r.break_even_revenue)}\nContribution Margin: $${formatNum(r.contribution_margin)} (${r.contribution_margin_pct}%)`);
});

$('#roi-calc').addEventListener('click', async () => {
    const r = await api('/api/financial/roi', {
        investment: parseFloat($('#roi-invest').value),
        return_value: parseFloat($('#roi-return').value),
        years: parseFloat($('#roi-years').value),
    });
    if (r.error) { showResult('#roi-result', 'Error: ' + r.error); return; }
    showResult('#roi-result', `ROI: ${r.roi}%\nAnnualized ROI: ${r.annualized_roi}%\nTotal Return: $${formatNum(r.total_return)}`);
});

$('#margin-calc').addEventListener('click', async () => {
    const r = await api('/api/financial/profit_margin', {
        revenue: parseFloat($('#margin-revenue').value),
        cost: parseFloat($('#margin-cost').value),
    });
    if (r.error) { showResult('#margin-result', 'Error: ' + r.error); return; }
    showResult('#margin-result', `Gross Profit: $${formatNum(r.gross_profit)}\nGross Margin: ${r.gross_margin}%\nMarkup: ${r.markup}%`);
});

/* ===== BUTTON EVENT DISPATCHING ===== */
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const mode = currentMode;
        const action = btn.dataset.action;
        const value = btn.dataset.value;
        const base = btn.dataset.base;

        /* Mode-agnostic buttons */
        if (base) {
            progBase = parseInt(base);
            updateProgDisplay();
            return;
        }

        if (mode === 'standard') {
            if (action) { stdAction(action); return; }
            if (value !== undefined) {
                if (newNumber && value >= '0' && value <= '9') { result = value; newNumber = false; }
                else if (newNumber && value === '.') { result = '0.'; newNumber = false; }
                else if ('+-*/'.includes(value)) {
                    expression += result + value;
                    result = '0';
                    newNumber = true;
                } else {
                    if (result === '0' && value !== '.') result = value;
                    else result += value;
                    newNumber = false;
                }
                updateStdDisplay();
            }
        } else if (mode === 'scientific') {
            if (action) { sciAction(action); return; }
            if (value !== undefined) {
                if (newNumber && value >= '0' && value <= '9') { result = value; newNumber = false; }
                else if (newNumber && value === '.') { result = '0.'; newNumber = false; }
                else if ('+-*/'.includes(value)) {
                    expression += result + value;
                    result = '0';
                    newNumber = true;
                } else if (value === '**') {
                    expression += result + '**';
                    result = '0';
                    newNumber = true;
                } else {
                    if (result === '0' && value !== '.') result = value;
                    else result += value;
                    newNumber = false;
                }
                updateSciDisplay();
            }
        } else if (mode === 'programmer') {
            if (action) { progAction(action); return; }
            if (value !== undefined) {
                if ('0123456789ABCDEF'.includes(value.toUpperCase())) {
                    progDigit(value.toUpperCase());
                } else if ('+-*'.includes(value)) {
                    progOp(value === '*' ? '*' : value);
                }
            }
        }
    });
});

/* ===== KEYBOARD SUPPORT ===== */
document.addEventListener('keydown', (e) => {
    const key = e.key;
    if (currentMode === 'standard' || currentMode === 'scientific') {
        if (key >= '0' && key <= '9' || key === '.') {
            const btn = $(`#page-${currentMode} .btn.num[data-value="${key}"]`);
            if (btn) btn.click();
        } else if (key === '+') { const btn = $(`#page-${currentMode} .btn.op[data-value="+"]`); if (btn) btn.click(); }
        else if (key === '-') { const btn = $(`#page-${currentMode} .btn.op[data-value="-"]`); if (btn) btn.click(); }
        else if (key === '*') { const btn = $(`#page-${currentMode} .btn.op[data-value="*"]`); if (btn) btn.click(); }
        else if (key === '/') { e.preventDefault(); const btn = $(`#page-${currentMode} .btn.op[data-value="/"]`); if (btn) btn.click(); }
        else if (key === 'Enter' || key === '=') { e.preventDefault(); stdAction('calculate'); }
        else if (key === 'Backspace') { stdAction('backspace'); }
        else if (key === 'Escape') { stdAction('clear'); }
        else if (key === 'Delete') { stdAction('ce'); }
    }
});

/* ===== INIT ===== */
updateStdDisplay();
