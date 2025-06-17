
def process_student_data():
    # 這是一段結構混亂的程式碼，混合了所有邏輯
    
    # 步驟1: 定義原始資料
    student_grades_str = "小明:85,小華:92,小李:78,小張:65,小王:45"
    
    # 步驟2: 解析字串並計算總分
    total_score = 0
    student_count = 0
    names = []
    grades_data = student_grades_str.split(',')
    
    print("--- 成績報告 ---")
    for item in grades_data:
        name, score_str = item.split(':')
        score = int(score_str)
        
        # 步驟3: 判斷每個學生的等第
        grade_level = ''
        if score >= 90:
            grade_level = 'A'
        elif score >= 80:
            grade_level = 'B'
        elif score >= 70:
            grade_level = 'C'
        elif score >= 60:
            grade_level = 'D'
        else:
            grade_level = 'F'
            
        print(f"學生: {name}, 分數: {score}, 等第: {grade_level}")
        
        total_score += score
        student_count += 1
        names.append(name)
        
    # 步驟4: 計算並印出平均分數
    average_score = total_score / student_count
    print("\n--- 總結 ---")
    print(f"總人數: {student_count} 人")
    print(f"班級總分: {total_score} 分")
    print(f"班級平均分數: {average_score:.2f} 分")

# 執行主函式
process_student_data()

