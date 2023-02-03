# Chpater 13 : Machine Translation

__13.1__ Compute by hand the chrF2,2 score for HYP2 on page 261 (the answer should round to 0.62).

| Type         | Text Data             |
|--------------|-----------------------|
| Reference    | witness for the past, |
| Hypothesis 1 | witness of the past,  |
| Hypothesis 2 | past witness          |

See chrF.py for calculations.
```
1-gram chrP:        17 / 17 = 1.0
1-gram chrR:        17 / 18 = 0.9444444444444444
2-gram chrP:        13 / 16 = 0.8125
2-gram chrR:        13 / 17 = 0.7647058823529411
reference:  witness for the past,
hypothesis: witness of the past,
chrF:       0.8644332482217764 = 0.86

1-gram chrP:        11 / 11 = 1.0
1-gram chrR:        11 / 18 = 0.6111111111111112
2-gram chrP:        9 / 10 = 0.9
2-gram chrR:        9 / 17 = 0.5294117647058824
reference:  witness for the past,
hypothesis: past witness
chrF:       0.619812308382562 = 0.62
```
