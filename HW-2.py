import numpy as np
personscore=np.dtype({
    'names':['name','chinese','math','english'],
    'formats':['S32','i','i','i']
}
)
peoples=np.array([('ZhangFei',68,65,30),('GuanYu',95,76,98),('LiuBei',98,86,88),('DianWei',90,88,77),('XuShu',80,90,90)],dtype=personscore)
chineses=peoples['chinese']
maths=peoples['math']
englishs=peoples['english']
print('语文平均值为：%f'%np.mean(chineses))
print('数学平均值为：%f'%np.mean(maths))
print('英语平均值为：%f'%np.mean(englishs))

print('语文最小值为：%i'%np.min(chineses))
print('数学最小值为：%i'%np.min(maths))
print('英语最小值为：%i'%np.min(englishs))

print('语文最大值为：%i'%np.max(chineses))
print('数学最大值为：%i'%np.max(maths))
print('英语最大值为：%i'%np.max(englishs))

print('语文方差为：%f'%np.var(chineses))
print('数学方差为：%f'%np.var(maths))
print('英语方差为：%f'%np.var(englishs))

print('语文标准差为：%f'%np.std(chineses))
print('数学标准差为：%f'%np.std(maths))
print('英语标准差为：%f'%np.std(englishs))

ranking = sorted(peoples,key=lambda x:x[1]+x[2]+x[3], reverse=True)
print(ranking)
