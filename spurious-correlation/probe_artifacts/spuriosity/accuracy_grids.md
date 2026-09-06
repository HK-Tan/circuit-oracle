# Probe Accuracy Grids

Biased vs. unbiased probe accuracy by subgroup, structured as Target × Spurious.
```
┌────────────┬────────────┐
│ Spurious=0 │ Spurious=1 │                       
│ Target=0   │ Target=0   │
├────────────┼────────────┤
│ Spurious=0 │ Spurious=1 │
│ Target=1   │ Target=1   │
└────────────┴────────────┘
```
---

## bib_nurse_professor
*(target: nurse=1 · spurious: female=1)*

```
┌──────────────────────────┬──────────────────────────┐
│  male professor          │  female professor        │
│  Biased:   98.9%         │  Biased:   17.6%         │
│  Unbiased: 97.8%         │  Unbiased: 97.2%         │
│  n = 16,205              │  n = 13,315              │
├──────────────────────────┼──────────────────────────┤
│  male nurse              │  female nurse            │
│  Biased:   12.7%         │  Biased:   96.9%         │
│  Unbiased: 82.0%         │  Unbiased: 74.5%         │
│  n = 434                 │  n = 4,304               │
└──────────────────────────┴──────────────────────────┘
```

---

## bib_journalist_dietitian
*(target: dietitian=1 · spurious: female=1)*

```
┌──────────────────────────┬──────────────────────────┐
│  male journalist         │  female journalist       │
│  Biased:   99.8%         │  Biased:   64.3%         │
│  Unbiased: 88.2%         │  Unbiased: 93.8%         │
│  n = 2,518               │  n = 2,468               │
├──────────────────────────┼──────────────────────────┤
│  male dietitian          │  female dietitian        │
│  Biased:   25.4%         │  Biased:   97.6%         │
│  Unbiased: 95.8%         │  Unbiased: 95.3%         │
│  n = 71                  │  n = 918                 │
└──────────────────────────┴──────────────────────────┘
```

---

## bib_surgeon_teacher
*(target: teacher=1 · spurious: female=1)*

```
┌──────────────────────────┬──────────────────────────┐
│  male surgeon            │  female surgeon          │
│  Biased:   4.9%          │  Biased:   0.4%          │
│  Unbiased: 3.8%          │  Unbiased: 4.2%          │
│  n = 2,894               │  n = 504                 │
├──────────────────────────┼──────────────────────────┤
│  male teacher            │  female teacher          │
│  Biased:   9.6%          │  Biased:   87.8%         │
│  Unbiased: 8.1%          │  Unbiased: 9.0%          │
│  n = 1,611               │  n = 2,440               │
└──────────────────────────┴──────────────────────────┘
```

---

## civil_comments
*(target: toxic=1 · spurious: identity-attack=1)*

```
┌────────────────────────────────┬────────────────────────────────┐
│  non-toxic, no identity-attack │  non-toxic, +identity-attack   │
│  Biased:   84.5%               │  Biased:   17.8%               │
│  Unbiased: 62.7%               │  Unbiased: 44.6%               │
│  n = 354                       │  n = 354                       │
├────────────────────────────────┼────────────────────────────────┤
│  toxic, no identity-attack     │  toxic, +identity-attack       │
│  Biased:   41.5%               │  Biased:   90.4%               │
│  Unbiased: 85.6%               │  Unbiased: 71.5%               │
│  n = 354                       │  n = 354                       │
└────────────────────────────────┴────────────────────────────────┘
  Spurious pattern: PARTIAL
```

---

## multinli
*(target: contradiction=1 · spurious: negation=1)*

```
┌────────────────────────────────┬────────────────────────────────┐
│  entailment, no negation       │  entailment, +negation         │
│  Biased:   97.4%               │  Biased:   39.5%               │
│  Unbiased: 72.9%               │  Unbiased: 88.0%               │
│  n = 266                       │  n = 266                       │
├────────────────────────────────┼────────────────────────────────┤
│  contradiction, no negation    │  contradiction, +negation      │
│  Biased:   18.0%               │  Biased:   86.5%               │
│  Unbiased: 71.1%               │  Unbiased: 73.7%               │
│  n = 266                       │  n = 266                       │
└────────────────────────────────┴────────────────────────────────┘
```


  Summary:        
```
  ┌──────────────────────────┬──────────────────────────┐
  │         Dataset          │          Works?          │
  ├──────────────────────────┼──────────────────────────┤
  │ bib_nurse_professor      │ ✓                        │
  ├──────────────────────────┼──────────────────────────┤
  │ bib_journalist_dietitian │ ✓ (mild TR degradation)  │
  ├──────────────────────────┼──────────────────────────┤
  │ bib_surgeon_teacher      │ ✗ probes learned nothing │ ├──────────────────────────┼──────────────────────────┤
  │ civil_comments           │ ✗ non-toxic rows broken  │
  ├──────────────────────────┼──────────────────────────┤
  │ multinli                 │ ✗ unbiased degenerates   │
  └──────────────────────────┴──────────────────────────┘ 
  ```