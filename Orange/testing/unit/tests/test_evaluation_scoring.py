import random
from Orange import data
from Orange.evaluation import scoring, testing
from Orange.statistics import distribution

try:
    import unittest2 as unittest
except:
    import unittest

random.seed(0)
def random_learner(data, *args):
    def random_classifier(*args, **kwargs):
        prob = [random.random() for _ in data.domain.class_var.values]
        sprob = sum(prob)
        prob = [i / sprob for i in prob]
        distribution.Discrete(prob)
        return data.domain.class_var[random.randint(0,
            len(data.domain.class_var.values) - 1)], prob
    return random_classifier

class TestAuc(unittest.TestCase):
    def setUp(self):
        self.learner = random_learner

    def test_auc_on_monks(self):
        ds = data.Table("monks-1")
        cv = testing.cross_validation([self.learner], ds, folds=5)
        pt = testing.proportion_test([self.learner], ds, times=1)

        auc = scoring.AUC(cv)
        self.assertEqual(len(auc), 1)

        auc = scoring.AUC(pt)
        self.assertEqual(len(auc), 1)

    def test_auc_on_iris(self):
        ds = data.Table("iris")
        test_results = testing.cross_validation([self.learner], ds, folds=5)
        auc = scoring.AUC(test_results)

        self.assertEqual(len(auc), 1)

    def test_auc_on_iris_by_pairs(self):
        ds = data.Table("iris")
        test_results = testing.cross_validation([self.learner], ds, folds=5)
        auc = scoring.AUC(test_results, multiclass=scoring.AUC.ByPairs)

        self.assertEqual(len(auc), 1)

    def test_auc_on_iris_by_weighted_pairs(self):
        ds = data.Table("iris")
        test_results = testing.cross_validation([self.learner], ds, folds=5)
        auc = scoring.AUC(test_results, multiclass=scoring.AUC.ByWeightedPairs)

        self.assertEqual(len(auc), 1)

    def test_auc_on_iris_one_against_all(self):
        ds = data.Table("iris")
        test_results = testing.cross_validation([self.learner], ds, folds=5)
        auc = scoring.AUC(test_results, multiclass=scoring.AUC.OneAgainstAll)

        self.assertEqual(len(auc), 1)

    def test_auc_on_iris_weighted_one_against_all(self):
        ds = data.Table("iris")
        test_results = testing.cross_validation([self.learner], ds, folds=5)
        auc = scoring.AUC(test_results, multiclass=scoring.AUC.WeightedOneAgainstAll)

        self.assertEqual(len(auc), 1)

    def test_auc_on_iris_single_class(self):
        ds = data.Table("iris")
        test_results = testing.cross_validation([self.learner], ds, folds=5)
        auc = scoring.AUC_for_single_class(test_results)
        self.assertEqual(len(auc), 1)
        auc = scoring.AUC_for_single_class(test_results, 0)
        self.assertEqual(len(auc), 1)
        auc = scoring.AUC_for_single_class(test_results, 1)
        self.assertEqual(len(auc), 1)
        auc = scoring.AUC_for_single_class(test_results, 2)
        self.assertEqual(len(auc), 1)

    def test_auc_on_iris_pair(self):
        ds = data.Table("iris")
        test_results = testing.cross_validation([self.learner], ds, folds=5)
        auc = scoring.AUC_for_pair_of_classes(test_results, 0, 1)
        self.assertEqual(len(auc), 1)
        auc = scoring.AUC_for_pair_of_classes(test_results, 0, 2)
        self.assertEqual(len(auc), 1)
        auc = scoring.AUC_for_pair_of_classes(test_results, 1, 2)
        self.assertEqual(len(auc), 1)

    def test_auc_matrix_on_iris(self):
        ds = data.Table("iris")
        test_results = testing.cross_validation([self.learner], ds, folds=5)
        auc = scoring.AUC_matrix(test_results)
        self.assertEqual(len(auc), 1)
        self.assertEqual(len(auc[0]), 3)


class TestCA(unittest.TestCase):
    def setUp(self):
        self.learner = random_learner

    def test_ca_on_iris(self):
        ds = data.Table("iris")
        cv = testing.cross_validation([self.learner], ds, folds=5)
        ca = scoring.CA(cv)
        self.assertEqual(len(ca), 1)

    def test_ca_from_confusion_matrix_list_on_iris(self):
        ds = data.Table("iris")
        cv = testing.cross_validation([self.learner], ds, folds=5)
        cm = scoring.confusion_matrices(cv)
        ca = scoring.CA(cm)
        self.assertEqual(len(ca), 1)

    def test_ca_from_confusion_matrix_on_iris(self):
        ds = data.Table("iris")
        cv = testing.cross_validation([self.learner], ds, folds=5)
        cm = scoring.confusion_matrices(cv, class_index=1)
        ca = scoring.CA(cm[0])
        self.assertEqual(len(ca), 1)

    def test_ca_from_confusion_matrix_for_classification_on_iris(self):
        ds = data.Table("iris")
        pt = testing.proportion_test([self.learner], ds, times=1)
        self.assertEqual(pt.number_of_iterations, 1)
        ca = scoring.CA(pt)
        self.assertEqual(len(ca), 1)

    def test_ca_from_confusion_matrix_for_classification_on_iris_se(self):
        ds = data.Table("iris")
        pt = testing.proportion_test([self.learner], ds, times=1)
        self.assertEqual(pt.number_of_iterations, 1)
        ca = scoring.CA(pt, report_se=True)
        self.assertEqual(len(ca), 1)

    def test_ca_from_confusion_matrix_on_iris_se(self):
        ds = data.Table("iris")
        cv = testing.cross_validation([self.learner], ds, folds=5)
        cm = scoring.confusion_matrices(cv, class_index=1)
        ca = scoring.CA(cm[0], report_se=True)
        self.assertEqual(len(ca), 1)

    def test_ca_on_iris(self):
        ds = data.Table("iris")
        cv = testing.cross_validation([self.learner], ds, folds=5)
        ca = scoring.CA(cv, report_se=True)
        self.assertEqual(len(ca), 1)


class TestConfusionMatrix(unittest.TestCase):
    def test_construct_confusion_matrix_from_multiclass(self):
        learner = random_learner
        ds = data.Table("iris")
        pt = testing.proportion_test([learner], ds, times=1)
        cm = scoring.confusion_matrices(pt)

        self.assertTrue(isinstance(cm[0], list))


    def test_construct_confusion_matrix_from_biclass(self):
        learner = random_learner
        ds = data.Table("monks-1")
        pt = testing.proportion_test([learner], ds, times=1)
        cm = scoring.confusion_matrices(pt, class_index=1)

        self.assertTrue(hasattr(cm[0], "TP"))

class CMScoreTest(object):
    def test_with_test_results_on_biclass(self):
        learner = random_learner
        ds = data.Table("monks-1")
        pt = testing.proportion_test([learner], ds, times=1)
        scores = self.score(pt)
        self.assertIsInstance(scores, list)

    def test_with_test_results_on_multiclass(self):
        learner = random_learner
        ds = data.Table("iris")
        pt = testing.proportion_test([learner], ds, times=1)

        scores = self.score(pt)
        self.assertIsInstance(scores, list)

    def test_with_confusion_matrices_on_biclass(self):
        learner = random_learner
        ds = data.Table("monks-1")
        pt = testing.proportion_test([learner], ds, times=1)
        cm = scoring.confusion_matrices(pt, class_index=1)
        scores = self.score(cm)
        self.assertIsInstance(scores, list)

    def test_with_confusion_matrices_on_multiclass(self):
        learner = random_learner
        ds = data.Table("iris")
        pt = testing.proportion_test([learner], ds, times=1)
        cm = scoring.confusion_matrices(pt, class_index=1)
        scores = self.score(cm)
        self.assertIsInstance(scores, list)

    def test_with_confusion_matrix_on_biclass(self):
        learner = random_learner
        ds = data.Table("monks-1")
        pt = testing.proportion_test([learner], ds, times=1)
        cm = scoring.confusion_matrices(pt, class_index=1)
        scores = self.score(cm[0])
        self.assertIsInstance(scores, float)

    def test_with_confusion_matrix_on_multiclass(self):
        learner = random_learner
        ds = data.Table("iris")
        pt = testing.proportion_test([learner], ds, times=1)
        cm = scoring.confusion_matrices(pt, class_index=1)
        scores = self.score(cm[0])
        self.assertIsInstance(scores, float)


class TestSensitivity(CMScoreTest, unittest.TestCase):
    @property
    def score(self):
        return scoring.Sensitivity

class TestSpecificity(CMScoreTest, unittest.TestCase):
    @property
    def score(self):
        return scoring.Specificity

class TestPrecision(CMScoreTest, unittest.TestCase):
    @property
    def score(self):
        return scoring.Precision

class TestRecall(CMScoreTest, unittest.TestCase):
    @property
    def score(self):
        return scoring.Recall

class TestPPV(CMScoreTest, unittest.TestCase):
    @property
    def score(self):
        return scoring.PPV

class TestNPV(CMScoreTest, unittest.TestCase):
    @property
    def score(self):
        return scoring.NPV

class TestF1(CMScoreTest, unittest.TestCase):
    @property
    def score(self):
        return scoring.F1

class TestFalpha(CMScoreTest, unittest.TestCase):
    @property
    def score(self):
        return scoring.Falpha

class TestMCC(CMScoreTest, unittest.TestCase):
    @property
    def score(self):
        return scoring.MCC


class TestUtils(unittest.TestCase):
    def test_split_by_classifier(self):
        learners = [random_learner, random_learner, random_learner]
        ds = data.Table("lenses")
        cv = testing.cross_validation(learners, ds, folds=5, store_examples=True)
        cv_split = scoring.split_by_classifiers(cv)
        ca_scores = scoring.CA(cv)
        auc_scores = scoring.AUC(cv)
        for i, cv1 in enumerate(cv_split):
            self.assertEqual(cv1.class_values, cv.class_values)
            self.assertEqual(cv1.classifier_names, [cv.classifier_names[i]])
            self.assertEqual(cv1.number_of_iterations, cv.number_of_iterations)
            self.assertEqual(cv1.number_of_learners, 1)
            self.assertEqual(cv1.base_class, cv.base_class)
            self.assertEqual(cv1.weights, cv.weights)
            self.assertEqual(len(cv1.results), len(cv.results))
            self.assertEqual(cv1.examples, cv.examples)

            ca_one = scoring.CA(cv1)[0]
            auc_one = scoring.AUC(cv1)[0]
            self.assertAlmostEqual(ca_scores[i], ca_one, delta=1e-10)
            self.assertAlmostEquals(auc_scores[i], auc_one, delta=1e-10)


if __name__ == '__main__':
    unittest.main()
