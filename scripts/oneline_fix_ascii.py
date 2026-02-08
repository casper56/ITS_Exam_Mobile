import json; p='www/ITS_Python/questions_ITS_python.json'; d=json.load(open(p,'rb')); q='27. \u3010CH03-6\u3011\u4f60\u70ba\u5b78\u6821\u8a2d\u8a08\u4e86\u4e00\u500b Python \u61c9\u7528\u7a0b\u5f0f\uff0c\u5728 classroom \u7684\u6e05\u55ae\u4e2d\u5305\u542b\u4e86 60 \u4f4d\u540c\u5b78\u7684\u59d3\u540d\uff0c\u6700\u5f8c 3 \u540d\u662f\u73ed\u4e0a\u7684\u5e79\u90e8\u3002<br>
\u4f60\u9700\u8981\u5206\u5272\u6e05\u55ae\u5167\u5bb9\u986f\u793a\u9664\u4e86\u5e79\u90e8\u4ee5\u5916\u7684\u6240\u6709\u540c\u5b78\uff0c\u4f60\u53ef\u4ee5\u5229\u7528\u4ee5\u4e0b\u54ea\u4e8c\u500b\u7a0b\u5f0f\u78bc\u9054\u6210\uff1f<br>
\u53ef\u4ee5\u7b54\u6210\u56de\u7b54 Yes \uff0c \u4e0d\u80fd\u56de\u7b54\u56de\u7b54 No<pre><code class="language-python">1. classroom[0: -2] = _(\u9078\u9805 1)_
2. classroom[0: -3] = _(\u9078\u9805 2)_
3. classroom[1: -3] = _(\u9078\u9805 3)_
4. classroom[: -3] = _(\u9078\u9805 4)_
5. classroom[1: -3] = _(\u9078\u9805 5)_</code></pre>'; e='\u25cf \u5728\u9019\u500b\u60c5\u6cc1\u4e0b\uff0c`classroom[0: -3]` \u548c `classroom[: -3]` \u90fd\u53ef\u4ee5\u6b63\u78ba\u5730\u53d6\u5f97\u9664\u4e86\u6700\u5f8c 3 \u540d\u540c\u5b78\u4ee5\u5916\u7684\u6240\u6709\u540c\u5b78\u3002<br>
\u25cf \u56e0\u6b64\uff0c\u9078\u9805 2 \u548c\u9078\u9805 4 \u662f\u6b63\u78ba\u7684\u3002'; c='D1_\u8cc7\u6599\u578b\u5225\u8207\u904b\u7b97\u5b50'; [ (i.update({'question':q,'explanation':e,'category':c,'type':'multioption','options':['Yes|No']*5,'answer':[2,1,2,1,2]})) for i in d if i.get('id')==27]; json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=4); print('Fixed')
