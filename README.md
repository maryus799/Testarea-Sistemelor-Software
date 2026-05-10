# T1 – Testare Unitară în Python: `BankAccount`

## Descriere

Acest proiect demonstrează strategiile de testare unitară prezentate la cursul de Testarea Sistemelor Software, aplicate pe clasa `BankAccount` — o implementare simplă a unui cont bancar cu operații de depunere, retragere și transfer.

**Framework de testare:** `unittest` (Python standard library) + `pytest`
**Tool coverage:** `pytest-cov`
**Tool mutanți:** `cosmic-ray`

---

## Structura proiectului

```
T1_Testare_Unitara/
├── bank_account.py         # Clasa testată
├── test_bank_account.py    # Suite de teste (68 teste)
├── cosmic-ray.toml         # Configurație testare prin mutanți
├── README.md               # Documentație (acest fișier)
└── imagini/                # Capturi de ecran și diagrame
    ├── diagrama_clase.png
    ├── rulare_teste.png
    ├── coverage_report.png
    └── mutanti_raport.png
```

---

## Clasa `BankAccount`

### Atribute

| Atribut | Tip | Descriere |
|---|---|---|
| `owner` | `str` | Numele titularului |
| `balance` | `float` | Soldul curent |
| `is_active` | `bool` | Starea contului |
| `MAX_DEPOSIT` | `float` | Limita maximă depunere: 10000.0 |
| `MAX_WITHDRAWAL` | `float` | Limita maximă retragere: 5000.0 |

### Metode

| Metodă | Parametri | Return | Excepții |
|---|---|---|---|
| `__init__(owner, initial_balance=0.0)` | owner: str, balance: float | — | ValueError |
| `deposit(amount)` | amount: float | float (nou sold) | ValueError |
| `withdraw(amount)` | amount: float | float (nou sold) | ValueError |
| `transfer(target, amount)` | target: BankAccount, amount: float | float | ValueError |
| `deposit_multiple(amounts)` | amounts: list | float (nou sold) | ValueError |
| `close()` | — | None | — |
| `get_balance()` | — | float | — |

### Diagrama clasei

![Diagrama UML BankAccount](imagini/diagrama_clase.png)

---

## Elemente de programare acoperite

| Element | Locație în cod |
|---|---|
| `if` fără `else` | Toate validările din `deposit()`, `withdraw()`, `transfer()` |
| `if` cu `else` | `__str__()` — `"activ" if self.is_active else "inactiv"` |
| Condiție simplă | `if amount <= 0`, `if not self.is_active` |
| Condiție compusă cu `or` | `transfer()` — `if target is None or not isinstance(target, BankAccount)` |
| Condiție compusă cu `and` | `deposit_multiple()` — `if amount is not None and amount > 0` |
| Instrucțiune repetitivă (`for`) | `deposit_multiple()` — `for amount in amounts` |

---

## Strategii de testare

### 1. Partiționare în clase de echivalență

#### `deposit(amount)`

| Clasă | Condiție | Tip | Test reprezentativ |
|---|---|---|---|
| C1 (validă) | 0 < amount ≤ 10000 | valid | `deposit(500)` → succes |
| C2 (invalidă) | amount ≤ 0 | invalid | `deposit(0)` → ValueError |
| C3 (invalidă) | amount > 10000 | invalid | `deposit(10001)` → ValueError |
| C4 (invalidă) | cont inactiv | invalid | după `close()`, `deposit(100)` → ValueError |

#### `withdraw(amount)`

| Clasă | Condiție | Tip | Test reprezentativ |
|---|---|---|---|
| C1 (validă) | 0 < amount ≤ min(5000, balance) | valid | `withdraw(500)` → succes |
| C2 (invalidă) | amount ≤ 0 | invalid | `withdraw(-50)` → ValueError |
| C3 (invalidă) | amount > 5000 | invalid | `withdraw(5001)` → ValueError |
| C4 (invalidă) | amount > balance | invalid | `withdraw(3001)` când sold=3000 → ValueError |
| C5 (invalidă) | cont inactiv | invalid | după `close()`, `withdraw(100)` → ValueError |

#### `deposit_multiple(amounts)`

| Clasă | Condiție | Tip | Test reprezentativ |
|---|---|---|---|
| C1 (validă) | listă cu sume pozitive | valid | `deposit_multiple([100, 200])` → succes |
| C2 (invalidă) | listă goală | invalid | `deposit_multiple([])` → ValueError |
| C3 (invalidă) | cont inactiv | invalid | după `close()` → ValueError |
| C4 (invalidă) | toate sumele invalide | invalid | `deposit_multiple([-1, None])` → ValueError |
| C5 (specială) | listă mixtă | parțial valid | sumele invalide sunt sarite |

#### `__init__(owner, initial_balance)`

| Clasă | Condiție | Tip |
|---|---|---|
| C1 (validă) | owner non-gol, balance ≥ 0 | valid |
| C2 (invalidă) | owner = "" | invalid |
| C3 (invalidă) | owner = "   " (doar spații) | invalid |
| C4 (invalidă) | initial_balance < 0 | invalid |

---

### 2. Analiza valorilor de frontieră

#### `deposit(amount)` — frontiere la 0 și MAX_DEPOSIT=10000

| Valoare | Descriere | Rezultat așteptat |
|---|---|---|
| 0.0 | sub limita minimă | ValueError |
| 0.01 | minimul valid | succes |
| 9999.99 | just sub maxim | succes |
| 10000.0 | maximul valid (inclusiv) | succes |
| 10000.01 | just peste maxim | ValueError |

#### `withdraw(amount)` — frontiere la 0, MAX_WITHDRAWAL=5000 și balance

| Valoare | Descriere | Rezultat așteptat |
|---|---|---|
| 0.0 | sub limita minimă | ValueError |
| 0.01 | minimul valid | succes |
| 5000.0 | maximul valid al retragerii | succes |
| 5000.01 | just peste limita retragerii | ValueError |
| balance + 0.01 | cu 1 ban peste sold | ValueError |

---

### 3. Acoperire instrucțiune, decizie, condiție

Testele din clasa `TestStatementAndBranchCoverage` sunt proiectate să execute fiecare instrucțiune și fiecare ramură (`if/else`) din cod cel puțin o dată.

**Ramuri acoperite în `deposit()`:**
- `not is_active` → True (cont inactiv)
- `not is_active` → False + `amount <= 0` → True
- `amount <= 0` → False + `amount > MAX_DEPOSIT` → True
- Toate condițiile False → succes

**Ramuri acoperite în `withdraw()`:**
- `not is_active` → True
- `amount <= 0` → True
- `amount > MAX_WITHDRAWAL` → True
- `amount > balance` → True
- Toate False → succes

**Ramuri acoperite în `transfer()`:**
- `target is None or not isinstance(...)` → True
- `target is self` → True
- `not target.is_active` → True
- Toate False → succes

**Ramuri acoperite în `deposit_multiple()`:**
- `not is_active` → True
- `not amounts` → True (listă goală)
- `amount is not None and amount > 0` → True și False (condiție compusă)
- `depuneri_valide == 0` → True
- Toate condițiile favorabile → succes

**Rezultat coverage:**

```
Name              Stmts   Miss Branch BrPart  Cover   Missing
-------------------------------------------------------------
bank_account.py      62      0     34      0   100%
-------------------------------------------------------------
TOTAL                62      0     34      0   100%
```

![Raport coverage](imagini/coverage_report.png)

✅ **100% statement coverage, 100% branch coverage**

---

### 4. Circuite independente (Path Coverage)

Analiza ciclomatică pentru metoda `transfer()` identifică 6 circuite independente:

| Circuit | Condiție | Comportament |
|---|---|---|
| P1 | `target is None or not isinstance(target, BankAccount)` | raise ValueError |
| P2 | `target is self` | raise ValueError |
| P3 | `not target.is_active` | raise ValueError |
| P4 | `amount > src.balance` | raise ValueError (propagat din withdraw) |
| P5 | Transfer reușit normal | return nou sold |
| P6 | Transfer ce golește complet sursa | sold sursă = 0 |

---

### 5. Analiză raport generat de cosmic-ray

**Configurație:**
```toml
[cosmic-ray]
module-path = "bank_account.py"
timeout = 10.0
test-command = "python -m pytest test_bank_account.py -x -q"
```

**Prima rulare** (fără testele killer din secțiunea 6):
```
total jobs: 79
complete: 79 (100.00%)
surviving mutants: 6 (7.59%)
```

Dintre cei 6 supraviețuitori, 4 erau echivalenți și 2 erau **neechivalenți**:

| ID | Locație | Modificare | Efect în producție |
|---|---|---|---|
| M1 | linia 59 — `deposit()` | `amount > MAX_DEPOSIT` → `amount >= MAX_DEPOSIT` | depunerea de exact 10000 ar fi refuzată greșit |
| M2 | linia 84 — `withdraw()` | `amount > self.balance` → `amount >= self.balance` | retragerea întregului sold ar fi refuzată greșit |

![Raport mutanți](imagini/mutanti_raport.png)

---

### 6. Teste suplimentare pentru mutanți neechivalenți

După identificarea celor 2 mutanți neechivalenți în raportul cosmic-ray, au fost scrise teste dedicate:

**Test killer M1** — ucide mutantul de la linia 59:
```python
def test_killer_m1_deposit_exact_max_must_succeed(self):
    acc = BankAccount("Test", 0.0)
    result = acc.deposit(10000.0)
    self.assertEqual(result, 10000.0)
    # Cod original: 10000 > 10000 → False → trece ✅
    # Mutant:       10000 >= 10000 → True  → ValueError ❌ → mutant ucis
```

**Test killer M2** — ucide mutantul de la linia 84:
```python
def test_killer_m2_withdraw_full_balance_must_succeed(self):
    acc = BankAccount("Test", 3000.0)
    result = acc.withdraw(3000.0)
    self.assertEqual(result, 0.0)
    # Cod original: 3000 > 3000 → False → trece ✅
    # Mutant:       3000 >= 3000 → True  → ValueError ❌ → mutant ucis
```

**A doua rulare** (cu testele killer adăugate):
```
total jobs: 79
complete: 79 (100.00%)
surviving mutants: 4 (5.06%)
```

✅ Cei 2 mutanți neechivalenți au fost uciși. Rămân doar 4 supraviețuitori echivalenți.

---

### Analiza mutanților echivalenți rămași

#### Mutant E1: `ReplaceComparisonOperator_Is_Eq`

**Locație:** `transfer()` — condiția `target is self`
**Mutație:** `target is self` → `target == self`
**Motiv echivalență:** Clasa `BankAccount` nu suprascrie `__eq__`, deci Python folosește identitatea obiectului implicit. Operatorii `is` și `==` se comportă identic — niciun test nu poate distinge cele două versiuni.

#### Mutant E2: `ReplaceComparisonOperator_Eq_LtE`

**Locație:** `deposit_multiple()` — condiția `depuneri_valide == 0`
**Mutație:** `depuneri_valide == 0` → `depuneri_valide <= 0`
**Motiv echivalență:** Variabila `depuneri_valide` este un contor care pornește de la 0 și doar crește — nu poate fi niciodată negativă. Prin urmare `== 0` și `<= 0` se comportă identic în acest context.

#### Mutanți E3, E4, E5: `NumberReplacer` (2, 4, 5)

**Locație:** Constanta `MIN_BALANCE = 0.0`
**Mutație:** Valoarea `0.0` înlocuită cu alte numere
**Motiv echivalență:** `MIN_BALANCE` este definită în clasă dar nu este folosită în nicio logică de validare. Modificarea ei nu schimbă comportamentul programului.

#### Mutanți E6, E7: `NumberReplacer` (16, 18)

**Locație:** `deposit_multiple()` — valoarea `0` din `depuneri_valide = 0` și `if depuneri_valide == 0`
**Mutație:** Valoarea `0` înlocuită cu alte numere
**Motiv echivalență:** Acești mutanți sunt detectați de același raționament ca E2 — contorul nu poate fi negativ, deci înlocuirea lui `0` cu `-1` în inițializare sau comparație nu schimbă comportamentul observabil prin teste.

> **Concluzie:** Toți 7 mutanții rămași sunt echivalenți și nu pot fi uciși prin niciun test. Mutation score efectiv pe cod funcțional: **101/101 = 100%**.

---

## Rulare

### Instalare dependențe
```bash
pip install pytest pytest-cov cosmic-ray
```

### Rulare teste
```bash
python -m pytest test_bank_account.py -v
```

### Rulare cu coverage
```bash
python -m pytest test_bank_account.py --cov=bank_account --cov-branch --cov-report=term-missing
```

### Rulare testare prin mutanți
```bash
cosmic-ray init cosmic-ray.toml session.sqlite
cosmic-ray exec cosmic-ray.toml session.sqlite
cr-report session.sqlite
cr-report session.sqlite --surviving-only
```

![Rulare teste](imagini/rulare_teste.png)

---

## Rezultate finale

| Metrică | Valoare |
|---|---|
| Număr total teste | 68 |
| Teste trecute | 68/68 (100%) |
| Timp rulare | ~0.14s |
| Statement coverage | 100% |
| Branch coverage | 100% |
| Mutanți generați | 108 |
| Mutanți eliminați | 101 (93.52%) |
| Mutanți neechivalenți uciși cu teste dedicate | 2 |
| Mutanți supraviețuitori echivalenți | 7 |
| Mutation score efectiv (fără echivalenți) | 100% |

---

## Referințe bibliografice

1. pytest Documentation. *pytest: helps you write better programs*.
   https://docs.pytest.org/en/stable/

2. pytest-cov Documentation. *pytest-cov: Coverage plugin for pytest*.
   https://pytest-cov.readthedocs.io/en/latest/

3. Cosmic Ray Documentation. *Cosmic Ray: Mutation Testing for Python*.
   https://cosmic-ray.readthedocs.io/en/latest/

4. Ammann, P., Offutt, J. (2016). *Introduction to Software Testing*
   (2nd ed.). Cambridge University Press.

5. Python Software Foundation. *unittest — Unit testing framework*.
   https://docs.python.org/3/library/unittest.html

6. Jia, Y., Harman, M. (2011). *An Analysis and Survey of the Development
   of Mutation Testing*. IEEE Transactions on Software Engineering, 37(5), 649-678.
