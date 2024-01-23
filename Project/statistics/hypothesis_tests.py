import scipy.stats as stats


def is_normal(data, alpha=0.05):
    """
    Sprawdzenie normalności rozkładu danych.
    Zwraca True, jeśli dane są z rozkładu normalnego, w przeciwnym razie False.
    """
    stat, p_value = stats.normaltest(data)
    return p_value >= alpha


def is_homogeneous_variance(data1, data2, alpha=0.05):
    """
    Sprawdzenie równości wariancji między dwoma zbiorami danych.
    Zwraca True, jeśli wariancje są równe, w przeciwnym razie False.
    """
    stat, p_value = stats.bartlett(data1, data2)
    return p_value >= alpha


def is_dependent_t_test(data1, data2, alpha=0.05):
    """
    Sprawdzenie testu t dla zmiennych zależnych (sparowanych).
    Zwraca True, jeśli hipoteza zerowa jest odrzucana, w przeciwnym razie False.
    """
    stat, p_value = stats.ttest_rel(data1, data2)
    return p_value >= alpha


def is_independent_t_test(data1, data2, alpha=0.05):
    """
    Sprawdzenie testu t dla zmiennych niezależnych.
    Zwraca True, jeśli hipoteza zerowa jest odrzucana, w przeciwnym razie False.
    """
    stat, p_value = stats.ttest_ind(data1, data2)
    return p_value >= alpha


def is_one_way_anova(data_groups, alpha=0.05):
    """
    Sprawdzenie jednoczynnikowej analizy wariancji (ANOVA).
    Zwraca True, jeśli hipoteza zerowa jest odrzucana, w przeciwnym razie False.
    """
    stat, p_value = stats.f_oneway(*data_groups)
    return p_value >= alpha


def is_pearson_correlation(data1, data2, alpha=0.05):
    """
    Sprawdzenie współczynnika korelacji Pearsona.
    Zwraca True, jeśli hipoteza zerowa jest odrzucana, w przeciwnym razie False.
    """
    stat, p_value = stats.pearsonr(data1, data2)
    return p_value >= alpha


def is_spearman_rank_correlation(data1, data2, alpha=0.05):
    """
    Sprawdzenie współczynnika korelacji rangowej Spearmana.
    Zwraca True, jeśli hipoteza zerowa jest odrzucana, w przeciwnym razie False.
    """
    stat, p_value = stats.spearmanr(data1, data2)
    return p_value >= alpha


def is_mann_whitney_u_test(data1, data2, alpha=0.05):
    """
    Sprawdzenie testu U Manna-Whitneya dla dwóch niezależnych grup.
    Zwraca True, jeśli hipoteza zerowa jest odrzucana, w przeciwnym razie False.
    """
    stat, p_value = stats.mannwhitneyu(data1, data2)
    return p_value >= alpha


def is_repeated_measures_anova(data, alpha=0.05):
    """
    Sprawdzenie analizy wariancji z powtórzeniami (repeated measures ANOVA).
    Zwraca True, jeśli hipoteza zerowa jest odrzucana, w przeciwnym razie False.
    """
    stat, p_value = stats.friedmanchisquare(*data)
    return p_value >= alpha


def hypothesis_main(db_connector):
    property = db_connector.get_all_records("Property")
    data1 = property['sqm_price'].to_numpy()
    data2 = property['area'].to_numpy()
    data3 = property['sqm_price'].to_numpy() * property['area'].to_numpy()
    data_groups = [data1, data2, data3]

    print("Czy dane są z rozkładu normalnego?", is_normal(data1))
    print("Czy wariancje są równe?", is_homogeneous_variance(data1, data2))
    print("Czy t-test zależnych jest spełniony?", is_dependent_t_test(data1, data2))
    print("Czy t-test niezależnych jest spełniony?", is_independent_t_test(data1, data2))
    print("Czy ANOVA jest spełniona?", is_one_way_anova(data_groups))
    print("Czy korelacja Pearsona jest spełniona?", is_pearson_correlation(data1, data3))
    print("Czy U Mann-Whitneya jest spełniony?", is_mann_whitney_u_test(data1, data2))
    print("Czy analiza wariancji z powtórzeniami jest spełniona?", is_repeated_measures_anova([data1, data2, data3]))


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    from MYSQLConnector.connector import MYSQLConnector

    load_dotenv()

    db_connector = MYSQLConnector(
        os.getenv('DB_HOST'),
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('DB_NAME')
    )

    hypothesis_main(db_connector)