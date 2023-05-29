import pandas as pd
import warnings, os, re, random

warnings.filterwarnings("ignore")

# change dir
os.chdir(os.path.dirname(__file__))

# choose dataset
datasets = os.listdir("data")
dataset_map = {i:name.split(".")[0] for i, name in enumerate(datasets)}
for key, value in dataset_map.items():
    print(f"{key}: {value}")
dataset_id = input("choose number: ")
file = dataset_map[int(dataset_id)]
print(f'Get words from "{file}".\n')

# Get data
if file == "IELTS":
    file_path = os.path.join("data", f"{file}.xlsx")
    df = pd.read_excel(file_path, header=1)
    df.columns = ["English", "POS", "Definition", "Chinese"]
else:
    file_path = f"data/{file}.csv"
    df = pd.read_csv(file_path)

# choose the range of words
start = input(f"starting number(>=1, <={len(df)}) or word: ")
end = input(f"ending number(>{start}, <={len(df)}) or word: ")

if start.isdigit():
    start = int(start)
    end = int(end)
    df_test = df.iloc[start-1 : end]
else:
    df_test = df.copy()
    df_test.index = df_test["English"]
    df_test = df_test[start:end].reset_index(drop = True)
    start = 1
    end = len(df_test)

# choose test type
print("\n1: Questions in Chinese and answers in English.\n2: Questions in English and answers in Chinese.(Type)\n3: Questions in English and answers in Chinese.(Think)")
test_type = input("choose test type: ")

# start test
nums = list(range(start-1, end))
pattern = r'[，。！？；：“”‘’（）【】《》「」『』……——～·、]'
wrong = 0
while nums:
    print(f"{'_' * 150}")
    # choose a word
    if wrong == 0:
        num = random.choice(nums)
        nums.remove(num)
    else:
        num = nums.pop(0) # test the same word if previous round is wrong

    # get question and answer 
    if test_type == "1":
        quest = df_test.loc[num, "Chinese"]
        ans = df_test.loc[num, "English"]
    else:
        quest = df_test.loc[num, "English"]
        ans = df_test.loc[num, "Chinese"]
        ans1 = re.split(pattern, ans) # 標點號切割，之後判斷輸入值是否在切割的元素中
        ans1 = list(set(ans1) - set([""])) # 刪除空格

    pos = df_test.loc[num, "POS"]
    definition = df_test.loc[num, "Definition"]
    
    # test
    print(f"\nQuestion: {quest} ({pos})")
    print(f"Definition: {definition}")
    print(f"Remaining: {len(nums)+1} (No. {num})")
    if test_type != "3":
        ans_input = input("Answer: ")
        ans_input = ans_input.strip() # remove space
    else:
        input('Type "Enter" to check the answer...')
        print(f"\nAnswer: {ans}\n")
        print("0: Wrong\n1: Right")
        ans_input = input("choose result: ")

    # check answer
    wrong = 0
    if (test_type == "1") and (ans_input == ans):
        print(f"Right!!!")
    elif (test_type == "2") and (ans_input in ans1):
        print(f"Right!!!\nComplete answer: {ans}")
    elif (test_type == "3"):
        if ans_input == "0":
            nums.insert(0, num) # test the same word next round
            nums.append(num) # add this word to test again
            wrong = 1
    else:
        nums.insert(0, num) # test the same word next round
        nums.append(num) # add this word to test again
        wrong = 1
        print(f"Wrong!\nCorrect answer: {ans}")