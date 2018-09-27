# RefHelper
Tool that helps transform the article name to Bibtex or formatted reference string, especially useful for writing your essays.<br>
一个简单的工具，能够将您在写论文时随意记录的参考文献名自动转换为符合标准的参考文献格式或直接输出Bibtex文件

---
# Requirements
Python 3 (Basic requirement, you need to make sure `python` in Command window can work.)

# Tutorial
After downloading this repo, you need to create a text file with multiple article names in it. For example:<br>
[1]	Mobile charger billing system using lightweight Blockchain_Author1<br>
[2]	Decentralizing Privacy Using Blockchain to Protect Personal Data_Author2,Author3<br>
...<br>
If it is the first time you running this application, I suggest you running `requirements.bat` batch file in the root directory to install some basic packages.<br>
You can now run `run.bat` batch files to run the application. You need to specify the text file you just created and whether you want a Bibtex file or only formatted reference string. After a few minutes, you will get a well-formatted `.bib` file as follows:<br>
Christidis K, Devetsikiotis M. Blockchains and Smart Contracts for the Internet of Things[J]. IEEE Access, 2016, 4:2292-2303.<br>
Dorri A, Kanhere S S, Jurdak R, et al. Blockchain for IoT Security and Privacy: The Case Study of a Smart Home[C]// IEEE International Conference on Pervasive Computing and Communications Workshops. IEEE, 2017.<br>
...<br>
NOTICE: When you create the text file, it doesn't matter whether you put the authors before or after the article name. The program will automatically extract the name and author for you. But be aware, there must be a `_` between the article name and authors.<br>
NOTICE: When you use this program outside China Mainland, you may make a slight modification to the `main.py`. Just change `engine=baidu` to `engine=google` will work. But, if you change the engine to Google, you'll no longer able to export the formatted reference string.

# 教程
下载完成后，建议你首先运行一次`requirements.bat`批处理文件以准备一下基础的运行环境<br>
将本Repo下载到计算机后，首先需要你在程序根目录创建一个txt文件，文件中的内容应当类似下面的格式：<br>
[1]	基于区块链技术的采样机器人数据保护方法_赵赫<br>
[2]	5G移动通信发展趋势与若干关键技术_尤肖虎<br>
...<br>
当然，上面的格式也不是必须遵守的，作者名和文献名倒置、去除文献序号、甚至去掉作者的做法，本程序都是允许的！只要你遵守最基本的两个规定：有文献名、文献名和作者之间用`_`号隔开，程序就可以为您自动化转化标准格式。这也就意味着，你在写文章时，只需保留文献名，剩下的都可以在最后交给本程序来做。<br>
当准备完成这份文件后，我们假定其名为`test.txt`，接着便可以运行`run.bat`，程序会要求你输入文件名和是否输出格式化文献字串。本程序原生支持输出Bibtex文件或者可以直接复制word使用的格式化字符串（使用GB/T7714标准），Bibtex一般是留给用Latex写文章的同学使用的，若你不太懂怎么用Bibtex，程序询问时，你只需要输入`Y`就可以了。程序运行几分钟后便会输出一个`.bib`文件，里面内容如下：<br>
赵赫, 李晓风, 占礼葵,等. 基于区块链技术的采样机器人数据保护方法[J]. 华中科技大学学报(自然科学版), 2015, 43(s1):216-219.<br>
尤肖虎, 潘志文, 高西奇,等. 5G移动通信发展趋势与若干关键技术[J]. 中国科学:信息科学, 2014, 44(5):551-563.<br>
...<br>
上面的转换你在使用时根本无需知晓其原理，非常的简单易用。<br>
<br>
如果你有什么好的建议，欢迎在此提出Issue！
