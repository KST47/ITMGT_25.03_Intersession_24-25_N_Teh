#!/usr/bin/env python
# coding: utf-8

# ### Prompt:
# You are an analyst for a fastfood restaurant. The company has tasked you to analyze their past transactions. Each row represents a single transaction/order from one of their ten (10) branches. The order is recorded as a __`string`__ which is formatted as: 
# 
# "`[quantity1][item_code1], [quantity2][item_code2], [quantity3][item_code3]`"
# 
# However, because of some technical error, the __number of combo meals purchased__ as well as the __total order value__ was lost, so we'll need to restore that.
# 
# ### You are tasked to come up with the following:
# 1. Given the order column, count how many of each product was purchased
# 2. Given each product count, get the number of supposed combo meals purchased. <br><i>(You may update the product count when the combo meals are counted)</i>.
# 3. Calculate the total order value.
# 4. Determine which branch made the most revenue, and how much?
# 
# ### The combo meals are detailed below:
# 1. Family combo: 4 burgers, 4 fries, 4 drinks
# 2. Big combo: 1 burgers, 1 fries, 1 drinks
# 3. Snack combo: 1 fries, 1 drinks

# In[2]:


import pandas as pd
df = pd.read_csv("food_transactions.csv", index_col = 0)
df


# In[3]:


# 1. Given the order column, count how many of each product was purchased

def burger_counter(order):
    if type(order) == str and "S_Burger" in order:
        return int(order[order.find("S_Burger") - 1])
    else:
        return 0

def fries_counter(order):
    if type(order) == str and "S_Fries" in order:
        return int(order[order.find("S_Fries") - 1])
    else:
        return 0

def drink_counter(order):
    if type(order) == str and "S_Drink" in order:
        return int(order[order.find("S_Drink") - 1])
    else:
        return 0

df["No. of Burgers"] = df["order"].apply(burger_counter)
df["No. of Fries"] = df["order"].apply(fries_counter)
df["No. of Drinks"] = df["order"].apply(drink_counter)
df


# In[4]:


# 2. Given each product count, get the number of supposed combo meals purchased.
# (You may update the product count when the combo meals are counted).
# The combo meals are detailed below:
# Family combo: 4 burgers, 4 fries, 4 drinks
# Big combo: 1 burgers, 1 fries, 1 drinks
# Snack combo: 1 fries, 1 drinks

df["Fam_Combo_Burger"] = df["No. of Burgers"] // 4
df["Fam_Combo_Fries"] = df["No. of Fries"] // 4
df["Fam_Combo_Drink"] = df["No. of Drinks"] // 4
df["Family_Combo"] = df[["Fam_Combo_Burger", "Fam_Combo_Fries", "Fam_Combo_Drink"]].min(axis = 1)

df = df.drop("Fam_Combo_Burger", axis = 1)
df = df.drop("Fam_Combo_Fries", axis = 1)
df = df.drop("Fam_Combo_Drink", axis = 1)

df["placeholder_burger"] = df["No. of Burgers"] - 4 * df["Family_Combo"]
df["placeholder_fries"] = df["No. of Fries"] - 4 * df["Family_Combo"]
df["placeholder_drinks"] = df["No. of Drinks"] - 4 * df["Family_Combo"]
df["Big_Combo"] = df[["placeholder_burger", "placeholder_fries", "placeholder_drinks"]].min(axis = 1)

df = df.drop("placeholder_burger", axis = 1)
df = df.drop("placeholder_fries", axis = 1)
df = df.drop("placeholder_drinks", axis = 1)

df["placeholder_fries"] = df["No. of Fries"] - 4 * df["Family_Combo"] - df["Big_Combo"]
df["placeholder_drinks"] = df["No. of Drinks"] - 4 * df["Family_Combo"] - df["Big_Combo"]
df["Snack_Combo"] = df[["placeholder_fries", "placeholder_drinks"]].min(axis = 1)

df = df.drop("placeholder_fries", axis = 1)
df = df.drop("placeholder_drinks", axis = 1)

df["S_Burger"] = df["No. of Burgers"] - 4 * df["Family_Combo"] - df["Big_Combo"]
df["S_Fries"] = df["No. of Fries"] - 4 * df["Family_Combo"] - df["Big_Combo"] - df["Snack_Combo"]
df["S_Drink"] = df["No. of Drinks"] - 4 * df["Family_Combo"] - df["Big_Combo"] - df["Snack_Combo"]

df


# In[8]:


# 3. Calculate the total order value.

jsondf = pd.read_json("price_list.json")

df["Revenue"] = df["Family_Combo"] * jsondf["Fam_combo"] + df["Big_Combo"] * jsondf["Big_combo"] + df["Snack_Combo"] * jsondf["snack_combo"] + df["S_Burger"] * jsondf["S_Burger"] + df["S_Fries"] * jsondf["S_Fries"] + df["S_Drink"] * jsondf["S_Drink"]


# In[ ]:


# 4. Determine which branch made the most revenue, and how much?

df.groupby(["branch"]).sum(numeric_only = True)["Revenue"].sort_values(asecnding = False)

