#### ! 该分支停止维护，以后主要在God中进行统一维护，由于精力有限，所以这个以后只做demo参考使用
God详解

[TOC]

# God 

包含Ui Auto Test 、Api Auto Test

- Ui Auto Test : python  /selenium /unitest
- Api Auto Test: python /urllib2 /requests /unitest

将两个内容融合到一起了，不知道应该叫啥名字，故取名为：God

# 1.入口 

- ## ` Run.py`

## 1.1 命令行运行参数：

```python
python Run.py
```

## 1.2 通过命令行查看可传入参数：

```python
python Run.py -h
```



## 1.3 参数详细介绍

- 默认参数说明

  ```python
   -l: log        default    : warning 		# 定义控制台默认输出日志级别
   -b: brower     default    : phantomjs		# 定义Ui测试默认使用的浏览器
   -m: Main       default    : ui			    # 定义默认执行Ui自动化测试脚本
   -r: report     default    : true			# 定义默认生成测试报告
   -d: del_report default    : false			# 定义默认不删除本地生成的测试报告
   -u: backup     default    : false			# 定义本地代码默认不备份
   -e: email      default    : misc			# 定义邮件发送机制为：Misc
   -s: send_email default    : Null			# 定义发送给指定接收邮件人：Null
   -t: url_target default    : wanpinghui.com	 # 定义测试脚本的主域名是：www.wanpinghui.com
   -c: run_case   default:   : all			# 定义指定执行用例为all
   -a: all_case_name default : api		    # 查看全部可执行用例文件名称
   -n: run_case_file_name default:''			# 通过用例文件名称运行指定文件名用例
  ```

  ​

- 可选参数说明

  ```python
  -l  [ info   || debug  || error    || warning]
  ```

  日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET，例如：当前日志输出级别为：`info`则`debug`、`notset`级别的日志就不会输出

  ```python
  -b  [ chrome || firfox || phantomjs]
  ```

  目前内置3种浏览器driver配置，可根据环境主动选择

  ```python
  -m  [ ui     || api    || excel    ]
  ```

  设置当前执行的测试脚本：`ui`：代表执行UItest脚本；`api`:代表执行api测试脚本；`excel`：代表通过excel表格传入接口需要参数

  ```python
  -r  [ true   || false  ]
  ```

  设置是否生成测试报告

  ```python
  -d  [ true   || false  ]
  ```

  设置是否删除测试报告

  ```python
  -u  [ true   || false  ]
  ```

  设置是否备份当前代码

  ```python
  -e  [ true   || false  || misc     ]
  ```

  设置发送Email的三种机制：

  - `true`:一定发送邮件，即只要执行脚本就会发送邮件；此时支持指定发送给某人邮件

  - `false`：一定不发送邮件，即任何情况下，系统都不会执行发送邮件操作

  - `misc`：混合形式，即：

    1.测试脚本运行`fail` OR  `error` 的时候发送邮件

    2.命令行指定给某人发送邮件`python Run.py -s AAA@163.com`，此时发送邮件

    3.脚本执行次数 `times= 10` 时，发送邮件；（10次一循环）

  ```python
  -s [email_path]
  ```

  设置邮件发送个特定的人，其中`email_path `需要提前配置在`Email`库中才可以成为参数

  ```python
  -t  [ url_target  ]
  ```

  设置脚本执行环境，其中`url_target`支持：线上环境、线下环境

  ```python
   -c: [run_case]
  ```

  指定执行用例的小名，可单个执行，可多个用空格隔开执行

  ```python
   -a: [api|ui]
  ```

  查看全部可执行用例名称

  ```python
  -n [run_case_by_file_name]
  ```

  通过用例文件名称执行指定用例

# 2.路径结构

根目录中分为4个文件夹和`Run.py`：

- `Misc`: 存放一些开发过程中的重要记录，以及会用到的一些第三方库类的信息
- `Output`：存放框架运行的过程中所有产出
- `Setup`:存放Linux自动配置的shell脚本
- `Src`:主要的代码源，存放全部的生产代码

# 3. `Output`文件夹

包含：`Global`、`Log`、`SendReport`、`TestReport`、`Testdir`、`ScreenShot`

!* 这些产出文件夹不入库

- `Global`：存放的一些全局需要引用的参数，目前已txt的形式存放内容，每次运行脚本都会更新数据，起到一个中间存储器的功能
- `Log`:存放系统产生的Log日志，记录日志级别为：Debug
- `SendReport`:存放最新生成的测试报告
- `TestReport`:存放所有生成的测试报告
- `Testdir`:存放需要执行的用例脚本
- `ScreenShot`：存放Ui测试脚本中的截图

# 4.  `Src`源码文件夹

包含：`Conf` 、`Function`、`Lib`、`Play`、`TestCase`、`PublicMain.py`



### 4.1 `Conf`文件夹

配置文件夹，存放框架中全部可配置参数，其中：

- `ApiCaseSummary.yml`:配置Api全部用例
- `Config.yml`:框架主要配置文件，全部路径、全部域名
- `InitParameter.yml`:框架初始化配置文件，可配置本地开发环境和线上开发环境
- `UiCaseSummary.yml`:配置Ui全部用例

### 4.2 `Function`文件夹

框架方法文件夹，存放全部方法文件

- ApiMethod.py
- ApiSummary.py
- Email.py
- GlobalVariable.py
- LogMainClass.py
- MySql.py
- ReadConfig.py
- ReadExcel.py
- Report.py
- UiMethods.py
- Utils.py
- Xvfb.py

### 4.3 `Lib`文件夹

框架用到的第三方工具存放路径

### 4.4 `TestCase`文件夹

存放全部用例，包含Ui测试用例、Api测试用例

# 5.  `PublicMain.py`

主要的框架中心，内部代码运转流程如下：

- 开始测试=》
- 准备基础数据=》
- 创建所有路径=》
- 组织可执行用例=》
- 执行测试脚本=》
- 生成测试报告=》
- 发送测试报告=》
- 处理产出数据=》
- 完成测试
