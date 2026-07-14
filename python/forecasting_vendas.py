import pandas as pd
import numpy as np

try:
    from prophet import Prophet
    TEM_PROPHET = True
except ImportError:
    TEM_PROPHET = False


def carregar_serie_mensal(caminho_vendas="../vendas.csv"):
    df = pd.read_csv(caminho_vendas, parse_dates=["data_venda"])
    serie = (
        df.groupby(pd.Grouper(key="data_venda", freq="MS"))
        .size()
        .reset_index(name="vendas")
        .rename(columns={"data_venda": "ds", "vendas": "y"})
    )
    return serie


def treinar_e_projetar(serie, meses_futuro=6):
    if TEM_PROPHET:
        modelo = Prophet(yearly_seasonality=True, weekly_seasonality=False)
        modelo.fit(serie)
        futuro = modelo.make_future_dataframe(periods=meses_futuro, freq="MS")
        previsao = modelo.predict(futuro)
        resultado = previsao[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(meses_futuro)
    else:
        serie = serie.copy()
        serie["t"] = range(len(serie))
        coef = np.polyfit(serie["t"], serie["y"], 1)
        futuros_t = range(len(serie), len(serie) + meses_futuro)
        datas_futuras = pd.date_range(serie["ds"].max(), periods=meses_futuro + 1, freq="MS")[1:]
        yhat = [coef[0] * t + coef[1] for t in futuros_t]
        resultado = pd.DataFrame({
            "ds": datas_futuras,
            "yhat": yhat,
            "yhat_lower": [v * 0.85 for v in yhat],
            "yhat_upper": [v * 1.15 for v in yhat],
        })
    return resultado


def gerar_cenarios(previsao):
    cenarios = previsao.copy()
    cenarios["cenario_conservador"] = cenarios["yhat_lower"].round(0)
    cenarios["cenario_base"] = cenarios["yhat"].round(0)
    cenarios["cenario_otimista"] = cenarios["yhat_upper"].round(0)
    return cenarios[["ds", "cenario_conservador", "cenario_base", "cenario_otimista"]]


def calcular_erro_modelo(serie, meses_teste=6):
    treino = serie.iloc[:-meses_teste]
    teste = serie.iloc[-meses_teste:]
    previsto = treinar_e_projetar(treino, meses_futuro=meses_teste)

    y_real = teste["y"].values
    y_previsto = previsto["yhat"].values[:len(y_real)]

    mae = np.mean(np.abs(y_real - y_previsto))
    rmse = np.sqrt(np.mean((y_real - y_previsto) ** 2))
    return {"MAE": round(mae, 2), "RMSE": round(rmse, 2)}


if __name__ == "__main__":
    serie = carregar_serie_mensal()
    print(f"Série histórica: {len(serie)} meses de vendas\n")

    previsao = treinar_e_projetar(serie, meses_futuro=6)
    cenarios = gerar_cenarios(previsao)
    print("Projeção de vendas — próximos 6 meses (3 cenários):")
    print(cenarios.to_string(index=False))

    erro = calcular_erro_modelo(serie)
    print(f"\nValidação do modelo (últimos 6 meses reais vs. previstos):")
    print(f"  MAE  (erro médio absoluto): {erro['MAE']} vendas")
    print(f"  RMSE (raiz do erro quadrático médio): {erro['RMSE']} vendas")
    print("\n-> Sempre reporte esse erro junto com a projeção ao apresentar para a diretoria.")
