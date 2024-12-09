
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from collections import Counter
from sklearn.model_selection import  train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score,roc_auc_score, roc_curve
from sklearn.metrics import classification_report

class LogisticRegressionClassifier:
    def __init__(self, max_iter=200, lr = 0.01, tol = 0.001):
        self.max_iter = max_iter
        self.lr = lr
        self.tol = tol
        self.w = None
        self.b = None
        self.class_ = 2

    def sigmod(self,X):
        return 1 / (1 + np.exp(-X))

    def softmax(self,X):
        return np.exp(X)/np.sum(np.exp(X), axis=1,keepdims=True)

#极大似然估计： loss = -(y *(wx+b) - log(1+exp(wx+b)))
    def loss_lr(self,w,b,X,y):
        dot = np.dot(X,w) + b
        return -np.mean(y*dot - np.log(1+np.exp(dot)),axis=0)

    def loss_sofmax(self,w,b, X, y ):
        dot = np.dot(X,w) + b
        # print(self.softmax(dot)[0])
        # print(y[0])
        sdot = np.log(self.softmax(dot))
        return -np.sum(sdot*y)/X.shape[0]

    # dw = (y-sigmod(wx+b))*x
    # db = y-sigmod(wx+b)
    def dloss_lr(self,w,b,X,y):
        dot = np.dot(X,w) +b
        distance = (y-self.sigmod(dot)).reshape(-1,1)
        return np.mean(distance*X, axis=0), np.mean(distance,axis=0)

    def dloss_softmax(self,w,b,X,y):
        d = np.dot(X,w) + b
        y_hat = self.softmax(d)
        # print(y_hat)
        dw = -np.dot(X.T,(y_hat-y))/X.shape[0]
        db = np.mean(-(y_hat-y)/X.shape[0],axis=0)
        # print(db)
        return dw,db

        # return np.exp(d)/np.sum(np.exp(d))


    def fit(self,X,y):
        self.class_ = len(np.unique(y))
        m,n = X.shape[0],X.shape[1]
        if (self.class_ == 2):
            w = np.random.randn(n)
            b = np.random.randn(1)
            self.w, self.b = self.sgd_lr(w,b,X,y)
        else:
            class_ = len(np.unique(y))
            y = np.eye(class_)[y]
            w = np.random.normal(scale=0.01,size=(n,self.class_))
            b = np.ones(self.class_)
            self.w,self.b = self.sgd_softmax(w, b, X, y)
            print(self.w)
            print(self.b)

    def sgd_lr(self,w,b,X,y):
        for i in range(self.max_iter):
            dw,db = self.dloss_lr(w,b,X,y)
            w += self.lr*dw
            b += self.lr*db
            loss2 = self.loss_lr(w,b,X,y)
            print("epoch:{}: loss:{}".format(i, loss2))
            if(loss2 < self.tol):
                break
        return w,b

    def sgd_softmax(self, w, b, X, y):
        for i in range(self.max_iter):
            dw,db = self.dloss_softmax(w,b,X,y)
            w += self.lr * dw
            b += self.lr * db
            loss = self.loss_sofmax(w, b, X, y)
            print("epoch:{}: loss:{}".format(i, loss))
            if (loss < self.tol):
                break
        return w,b

    ###########################################################
    def predict_lr_proba(self, X):
        return self.sigmod(np.dot(X, self.w) + self.b)

    def predict_lr(self, X):
        return (self.sigmod(np.dot(X, self.w) + self.b)>0.5).astype(np.int_)

    def predict_softmax_proba(self, X):
        return self.softmax(np.dot(X, self.w)+self.b)

    def predict_softmax(self, X):
        return np.argmax(self.softmax(np.dot(X, self.w)+self.b),axis=1)





def plot_surface(clf,X, y):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1

    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01))
    X_test = np.c_[xx.ravel(), yy.ravel()]
    Z = clf.predict(X_test)>=0.5
    Z = Z.reshape(xx.shape)

    fig, ax = plt.subplots()
    counter = Counter(y)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel(feature_names[0])
    ax.set_ylabel(feature_names[1])
    ax.contourf(xx, yy, Z, cmap=plt.cm.RdYlBu)

    ## 画出分割线
    #     i = np.linspace(x_min, x_max, 100)
    #     o = (w[0] * i + b) / -w[1]
    #     ax.plot(i, o)

    for label in counter.keys():
        ax.scatter(X[y == label, 0], X[y == label, 1])
    plt.show()


def get_static_result(y_true, y_prd):
    print("precision:{}".format(precision_score(y_true,y_prd)))
    print("recall:{}".format(recall_score(y_true,y_prd)))
    print("f1_score:{}".format(f1_score(y_true,y_prd)))
    print("accuracy:{}".format(accuracy_score(y_true,y_prd)))
    print("auc:{}".format(roc_auc_score(y_true,y_prd)))

if __name__ == '__main__':
    clf = LogisticRegressionClassifier(max_iter=100000, lr=0.1)
    iris = load_iris()
    feature_names = iris.feature_names[2:]

    ## 2-class sigmod regression
    # X = iris.data[:100, :]
    # y = iris.target[:100]  # y \in {0, 1}
    # x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=123)
    # print("x_train:{}".format(x_train.shape))
    # print("x_test:{}".format(x_test.shape))
    # clf.fit(x_train,y_train)
    # y_prd = clf.predict_lr(x_test)
    # get_static_result(y_test,y_prd)

    X = iris.data[:, :]
    y = iris.target[:]  # y \in {0, 1}
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
    clf.fit(x_train, y_train)
    y_prd = clf.predict_softmax(x_train)
    y_true = y_train
    print("train acc:{}".format(accuracy_score(y_true, y_prd)))
    print(classification_report(y_true, y_prd))

    y_prd = clf.predict_softmax(x_test)
    y_true = y_test
    print("test acc:{}".format(accuracy_score(y_true, y_prd)))
    print(classification_report(y_true, y_prd))
    print(y_train[0:5])





