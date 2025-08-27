#### LogisticRegression

##### 问题

一组特征变量$\mathbb{x} = (x_1, x_2, \dots, x_m) \in \mathbb{R}^{n \times m}$，一组标签$\mathbb{y} = (y_1, y_2, \dots, y_m), y_i \in \{-1, +1 \}$

目标是估计条件概率$P(Y = 1 | X)$，即给定特征$X = x$的情况下，$y = 1$的概率。

##### 问题分析

如何用LogisticRegression做一个分类算法

1. 逻辑回归模型可以表示为

$$
z = \beta_0 + \beta_1x_1 + \beta_2x_2 + \dots + \beta_nx_n = \beta^T\mathbf{(1;x)}
$$

其中$\beta = (\beta_0, \beta_1, \dots\beta_n)^T, (1;x) = (1, x_1, x_2, \dots, x_n)^T$ 

2. 利用Sigmoid函数，将$z$变成概率

$$
h(x) = \sigma(z) = \frac{1}{1 + e^{-z}}
$$

这里$h(x)$表示：输入一个$x$，就可以判断这个$x$是$1$还是$0$



3. 训练目标：极大似然估计

* 对于每一个输入$x^{(i)}$，我们希望$\mathbb{P}(h(x^{(i)}) = y^{(i)})$越大越好，这样才比较准
* 因为$h(x^{(i)})$和$y^{(i)}$只有**1**和**0**两个取值，所以可以得到$\mathbb{P}(h(x^{(i)}) = y^{(i)}) = h(x^{(i)})^{y^{(i)}}(1 - h(x^{(i)}))^{y^{(i)}}$，对于这个式子怎么推导出来的，请自行带入$h(x^{(i)})$和$y^{(i)}$为1和0的四种情况
* 得到极大似然估计， 对于n个数据样本

$$
L(\beta) = \displaystyle\prod_{i=1}^n h(x^{(i)})^{y^{(i)}}(1 - h(x^{(i)}))^{y^{(i)}}
$$

* 负对数似然

$$
l(\beta) = -\sum_{i=1}^n \left[y^{(i)}log(h(x^{(i)})) + (1-y^{(i)})log(1-h(x^{(i)}))     \right]
$$



4. 优化方法

* 梯度下降法

$$
\beta_j := \beta_j + \alpha\frac{\partial l}{\partial \beta_j}
$$

$$
\frac{\partial l}{\partial \beta_j} = -\sum_{i=1}^n (h(x^{(i)}) - y^{(i)})x_j^{(i)}
$$

5. 加上正则化参数，然后整合

* 负对数似然，加上正则化参数

$$
l(\beta) = -\sum_{i=1}^n \left[y^{(i)}log(h(x^{(i)})) + (1-y^{(i)})log(1-h(x^{(i)}))     \right] + \frac{\lambda}{2}\sum_{i=1}^n \beta_i^2
$$

* 梯度下降的时候，加上正则化参数

$$
\frac{\partial l}{\partial \beta_j} = -\sum_{i=1}^n (h(x^{(i)}) - y^{(i)})x_j^{(i)} + \lambda\sum_{i=1}^n \beta_i
$$

* 参数修正后，这里的修正蕴含在上面的求导中

$$
\beta_j := \beta_j + \alpha\frac{\partial l}{\partial \beta_j}
$$
