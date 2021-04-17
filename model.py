import pickle


class PixelsClf:
    def __init__(self, model="model_0.96.knbclf"):
        with open(model, "rb") as file:
            self.clf = pickle.load(file)

    def predict(self, pixels: list[list[int]]) -> list[int]:
        """
        :param pixels: array of dims [N, 3] where each subarray if in the [R, G, B] format
        :return: array of zeros and ones where 2 is injured, 1 is not injured, 0 is everything else
        """
        return self.clf.predict(pixels)


if __name__ == '__main__':
    from learning import X_test, y_test

    clf = PixelsClf()
    print(clf.predict(X_test))
    print(y_test)
