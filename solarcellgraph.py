# モジュールのインポート 
import os, tkinter, tkinter.filedialog, tkinter.messagebox 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
# ファイル選択ダイアログの表示 
root = tkinter.Tk() 
root.withdraw() 

# ファイルの拡張子　
fTyp = [("","*")] 
fTyp = [("csv-file","*.csv"), ("All-file","*")] 
# フォルダパスを取得 
iDir = os.path.abspath(os.path.dirname(__file__)) 
tkinter.messagebox.showinfo('プログラム','ファイルを選択してください！') 
file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir) 
print(file) 
# ファイルパスの認識 
file1 = file.replace('/', os.sep) 
file_name = os.path.basename(file) 
data_path = os.path.dirname(file1) 
os.chdir(data_path) 
print(file_name) 

# csvファイル読み込み 
df = pd.read_csv(file_name, names=("Time","V","A"),skiprows=4,usecols=[0,1,2])#csvデータ読み込み
df= df.query("A <=0")

print(df)#読み込んだデータの確認表示用  

# mAをAに変換するやつ
def double_then_minus_5(x):
    x *= -1000
    x /= 0.1
    return x


df['A'] = df['A'].apply(double_then_minus_5)
#print(df['A'])#Aの値が変換できているかの確認のための行

df['W'] = df['V']*df['A']
#print(df['W'])

x = np.array(df['V']) 
y = np.array(df['A']) 


num = 0 # 値の指定

# 指定値に最も近い値のインデックスを取得
index1 = np.abs(x - num).argsort()[0].tolist()
index2 = np.abs(y - num).argsort()[0].tolist()

# 確認用
print("index number1: ", index1,"index number2: ", index2)

maxA=df['A'].max()
maxV=df['V'].max()
maxW=df['W'].max()
FF=maxW/(maxA*maxV)
nn=(maxW/100)*100

#　確認用
print({'開放電圧': maxV, '短絡電流': maxA, 'FF': FF, '変換効率': nn})

#グラフ化 
plt.title(file_name) 
plt.xlabel("Voltage(v)",size=15)
#横軸ラベル
plt.ylabel("Current density(mA/cm^2)",size=15)
#縦軸ラベル plt.grid(True)#目盛表示 
plt.tight_layout()
#全てのプロットをボックス内に 

plt.xlim([-0.2,1.2]) #ここでx軸の範囲を指定
plt.ylim([-5,22]) #ここでy軸の範囲を指定
plt.plot(x,y) 
plt.grid(color='r', linestyle='dotted', linewidth=1)

xmin, xmax = -5, 2
ymin, ymax = -20, 25
plt.hlines(0, xmin, xmax, colors='black')
plt.vlines(0, ymin, ymax, colors='black')





plt.show()
