::: titlepage
::: center
Санкт-Петербургский политехнический университет\
Петра Великого\
:::

::: center
Физико-механический иститут
:::

::: center
Кафедра «Прикладная математика»
:::

::: center
**Отчёт по курсовой работе\
по дисциплине «Анализ данных с интервальной неопределённостью»**
:::

::: flushleft
Выполнил студент:\
Аникин Александр Алексеевич\
группа: 5040102/20201

Проверил:\
к.ф.-м.н., доцент\
Баженов Александр Николаевич
:::

::: center
Санкт-Петербург\
2023 г.
:::
:::

# Постановка задачи

# Теория

## Точечная линейная регрессия

Рассматривается задача восстановления зависимости для выборки
$(X, \textbf(Y))$,
$X = \{x_i\}_{i=1}^{n}, \textbf{Y} = \{\textbf{y}_i\}_{i=1}^{n}$,
$x_i$ - точечный, $\textbf{y}_i$ - интервальный. Пусть искомая модель
задана в классе линейных функций

[]{#e:model label="e:model"} $$y = \beta_0 + \beta_1 x$$

Поставим задачу оптимизации [\[e:task\]](#e:task){reference-type="ref"
reference="e:task"} для нахождения точечных оценок параметров
$\beta_0, \beta_1$.

[]{#e:task label="e:task"} $$\begin{gathered}
            \sum_{i = 1}^{m}w_{i} \to \min \\
            \text{mid}\textbf{y}_{i} - w_{i} \cdot \text{rad}\textbf{y}_{i} \leq X\beta \leq \text{mid}\textbf{y}_{i} + w_{i} \cdot \text{rad}\textbf{y}_{i} \\
            w_{i} \geq 0, i = 1, ..., m \\
            w, \beta - ?
        \end{gathered}$$

Задачу [\[e:task\]](#e:task){reference-type="ref" reference="e:task"}
можно решить методами линейного программирования.

## Информационное множество

*Информационным множеством* задачи восстановления зависимости будем
называть множество значений всех параметров зависимости, совместных с
данными в каком-то смысле.

*Коридором совместных зависимостей* задачи восстановления зависимости
называется многозначное множество отображений $\Upsilon$, сопоставляющее
каждому значению аргумента $x$ множество

$$\Upsilon(x) = \bigcup_{\beta \in \Omega} f(x, \beta)$$

, где $\Omega$ - информационное множество, $x$ - вектор переменных,
$\beta$ - вектор оцениваемых параметров.

Информационное множество может быть построено как пересечение полос,
заданных

$$\underline{\textbf{y}_i} \leq \beta_0 + \beta_1 x_{i1} + ... + \beta_m x_{im} \leq \overline{\textbf{y}_i}$$
, где $i = \overline{1, n} \textbf{y}_i \in \textbf{Y}, x_i \in X$,
$X$ - точечная выборка переменных, $\textbf{Y}$ - интервальная выборка
откликов.

# Результаты

Данные были взяты из таблицы S1 приложенной к работе Roederer, Ian U.,
et al. \"Element abundance patterns in stars indicate fission of nuclei
heavier than uranium.\" Science 382.6675 (2023)

В ней представлены определенные значения для различных элементов и их
стандартные отклонения. В качестве $x$ выступает значение $[Eu/Fe]$, а в
качестве $y$ $X \pm eX,\ X \in \{Se, Sr, Y, Nb, Mo\}$. Эти данные
соответсвуют части данных с *рис Fig. 2. (A) Abundance ratios of groups
of elements that do or do not correlate with \[Eu/Fe\].* Остальные же
даные в материалах статьи представлены рядом ссылок, и автоматизировать
их сбор не представляется возможным.

Далее рассмотрим сами данные и получившие результаты.

<figure id="linreg">
<div class="center">
<img src="./doc/img/Se Sr Y Nb Mo.png" />
</div>
<figcaption> Синим цветом представлены значения для различных элементов
с их стандартными отклонениями. Оранжевым цветом показаны результаты
регрессии. </figcaption>
</figure>

Полученны $(\beta_1, \beta_2) = (-0.0, -0.9)$. Полученные результаты
отличаются от результатов в статье из-за отстутствия сдвига, однако
общий вывод будет одинаков из-за $\beta_1$ близкого к нулю.

Также стоит отметить что информационное множество пустое, так как
настоящая зависимость отличается от линейной и сами интвервалы
представляют собой лишь стандартное отклонение от среднего.

# Обсуждение

Можно сказать, что полученные результаты соответствуют результатам из
исходной работы с учетом отсутствия сдвига и меньшего количества данных.
Общий вывод об отсутствии линейной зависимости между значениями
сохраняется.