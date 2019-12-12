


languages = ['JavaScript', 'Python', 'Java', 'PHP', 'Go', 'Jupyter Notebook', 
             'HTML', 'Swift', 'TypeScript', 'Ruby', 'C++', 'CSS', 'Shell',
             'C', 'C#']

# raw counts by language

value_counts_by_language = []

for lang in languages:
    value_counts = pd.Series(' '.join(df[df.language==lang]['cleaned']).split()).value_counts()
    value_counts_by_language.append(value_counts)

plt.figure(figsize=(24,22))

plt.figure(figsize=(24, 22))
for i, lang in enumerate(value_counts_by_language):
    subplot(5, 3, i+1)
    lang.sort_values(ascending=False)[0:10].plot.barh(width=.9)
    title(f'Top 10 {languages[i]} words')


plt.legend()
plt.show()