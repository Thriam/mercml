from sklearn.linear_model import LinearRegression


X = [[1], [2], [3], [4], [5]]
y = [30, 50, 70, 90, 100]
model = LinearRegression()
model.fit(X,y)
print(model.predict([[6]]))
