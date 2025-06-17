
def calculate_sum_up_to(n):
    """
    這個函式應該要計算從 1 到 n (包含 n) 的所有整數總和。
    但是，它有一個隱藏的邏輯錯誤！
    """
    total = 0

    for i in range(n):
        total += i
        
    return total

# 測試案例
# 1 + 2 + 3 + 4 + 5 = 15，但程式會輸出 10
number_to_test = 5
expected_result = 15
actual_result = calculate_sum_up_to(number_to_test)

print(f"計算 1 到 {number_to_test} 的總和...")
print(f"預期結果應該是: {expected_result}")
print(f"程式實際算出: {actual_result}")

if actual_result != expected_result:
    print("\n哎呀！結果不對。請 AI 幫忙看看是哪裡出錯了吧！")
