import pandas as pd
import numpy as np

accounts = np.array([[1, 1, 3], [1, 2, 3], [1, 3, 1], [2, 2, 1], [2, 3, 1], [3, 1, 3], [4, 4, 1], [5, 5, 2]])

A = pd.DataFrame(accounts, columns=['account_id', 'item_id', 'rating'])

B = np.zeros((max(A.account_id), max(A.item_id)), dtype=int)

for account in accounts:
    account_id, item_id, rating = account
    B[account_id - 1][item_id - 1] = rating

B = pd.DataFrame(B, index=list(range(1, max(A.account_id) + 1)), columns=list(range(1, max(A.item_id) + 1)))
B