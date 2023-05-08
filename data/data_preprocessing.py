import re

# 留下字符与汉字
chinese = re.compile(r'[\u4E00-\u9FA5`~!@#$%^&*()_\-+=<>?:"{}|,.;·~！@#￥%……&*（）——\-+={}|《》？：“”【】、；‘，。、|\n]+')

fr = open('merge.txt', 'r', encoding='utf-8', errors='ignore')
fw = open('mer.txt', 'w', encoding='utf-8')
txt = fr.read()
for w in chinese.findall(txt):
    fw.write(w)
fr.close()
fw.close()
