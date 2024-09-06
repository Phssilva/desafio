import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px

from validate_docbr import CPF


BASE_URL = "http://backend_container:8000"


def get_produtores():
    response = requests.get(f"{BASE_URL}/produtores/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao buscar produtores.")
        return []


def create_produtor(data):
    response = requests.post(f"{BASE_URL}/produtores/", json=data)
    return response.json()


def update_produtor(id, data):
    response = requests.put(f"{BASE_URL}/produtores/{id}", json=data)
    return response.json()


def delete_produtor(id):
    response = requests.delete(f"{BASE_URL}/produtores/{id}")
    return response.json()


def is_valid_cpf(cpf):
    cpf_validator = CPF()
    return cpf_validator.validate(cpf)


def dashboard(produtores):
    st.subheader("Dashboard de Métricas")

    if not produtores:
        st.info("Nenhum dado disponível para exibir no dashboard.")
        return

    df = pd.DataFrame(produtores)

    # Métricas
    total_fazendas = len(df)
    total_area = df["area_total"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total de Fazendas", total_fazendas)
    col2.metric("Área Total (ha)", f"{total_area:,.2f}")

    st.markdown("---")

    st.subheader("Distribuição de Fazendas por Estado")
    estado_counts = df["estado"].value_counts().reset_index()
    estado_counts.columns = ["Estado", "Quantidade"]
    fig_estado = px.pie(
        estado_counts, names="Estado", values="Quantidade", title="Fazendas por Estado"
    )
    st.plotly_chart(fig_estado, use_container_width=True)

    st.subheader("Distribuição de Culturas Plantadas")
    culturas_exploded = df.explode("culturas_plantadas")  # contar individualmente
    cultura_counts = (
        culturas_exploded["culturas_plantadas"].value_counts().reset_index()
    )
    cultura_counts.columns = ["Cultura", "Quantidade"]
    fig_cultura = px.pie(
        cultura_counts, names="Cultura", values="Quantidade", title="Culturas Plantadas"
    )
    st.plotly_chart(fig_cultura, use_container_width=True)

    st.subheader("Distribuição de Uso de Solo")
    uso_solo = pd.DataFrame(
        {
            "Uso": ["Área Agricultável", "Área de Vegetação"],
            "Área (ha)": [df["area_agricultavel"].sum(), df["area_vegetacao"].sum()],
        }
    )
    fig_uso_solo = px.pie(
        uso_solo, names="Uso", values="Área (ha)", title="Uso de Solo"
    )
    st.plotly_chart(fig_uso_solo, use_container_width=True)


def main():
    st.set_page_config(page_title="Cadastro de Produtores Rurais", layout="wide")
    st.title("Cadastro de Produtores Rurais")

    menu = ["Dashboard", "Criar", "Ler", "Atualizar", "Deletar"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Dashboard":
        produtores = get_produtores()
        dashboard(produtores)

    elif choice == "Criar":
        st.subheader("Adicionar Novo Produtor")

        with st.form("produtor_form", clear_on_submit=True):
            cpf_cnpj = st.text_input("CPF ou CNPJ")
            nome_produtor = st.text_input("Nome do Produtor")
            nome_fazenda = st.text_input("Nome da Fazenda")
            cidade = st.text_input("Cidade")
            estado = st.text_input("Estado (UF)", max_chars=2)
            area_total = st.number_input("Área Total (ha)", min_value=0.0, step=0.01)
            area_agricultavel = st.number_input(
                "Área Agricultável (ha)", min_value=0.0, step=0.01
            )
            area_vegetacao = st.number_input(
                "Área de Vegetação (ha)", min_value=0.0, step=0.01
            )
            culturas = st.multiselect(
                "Culturas Plantadas",
                ["Soja", "Milho", "Algodão", "Café", "Cana de Açúcar"],
            )

            submit_button = st.form_submit_button("Cadastrar Produtor")

            if submit_button:
                if not is_valid_cpf(cpf_cnpj):
                    st.error("CPF inválido. Por favor, insira um CPF válido.")
                elif area_agricultavel + area_vegetacao > area_total:
                    st.error(
                        "A soma das áreas agricultável e vegetação não pode ser maior que a área total."
                    )
                elif not all(
                    [cpf_cnpj, nome_produtor, nome_fazenda, cidade, estado, culturas]
                ):
                    st.error("Todos os campos são obrigatórios.")
                else:
                    produtor_data = {
                        "cpf_cnpj": cpf_cnpj,
                        "nome_produtor": nome_produtor,
                        "nome_fazenda": nome_fazenda,
                        "cidade": cidade,
                        "estado": estado,
                        "area_total": area_total,
                        "area_agricultavel": area_agricultavel,
                        "area_vegetacao": area_vegetacao,
                        "culturas_plantadas": culturas,
                    }
                    result = create_produtor(produtor_data)
                    if isinstance(result, dict) and "detail" in result:
                        st.error(f"Erro ao cadastrar produtor: {result['detail']}")
                    else:
                        st.success("Produtor cadastrado com sucesso!")

    elif choice == "Ler":
        st.subheader("Lista de Produtores")

        produtores = get_produtores()
        if produtores:
            df = pd.DataFrame(produtores)
            st.dataframe(df)
        else:
            st.info("Nenhum produtor encontrado.")

    elif choice == "Atualizar":
        st.subheader("Atualizar Dados do Produtor")

        produtores = get_produtores()
        produtor_ids = [prod["id"] for prod in produtores]
        selected_id = st.selectbox("Selecione o Produtor", produtor_ids)

        if selected_id:
            produtor_data = next(
                (prod for prod in produtores if prod["id"] == selected_id), None
            )

            if produtor_data:
                with st.form("update_form", clear_on_submit=True):
                    cpf_cnpj = st.text_input(
                        "CPF ou CNPJ", value=produtor_data["cpf_cnpj"]
                    )
                    nome_produtor = st.text_input(
                        "Nome do Produtor", value=produtor_data["nome_produtor"]
                    )
                    nome_fazenda = st.text_input(
                        "Nome da Fazenda", value=produtor_data["nome_fazenda"]
                    )
                    cidade = st.text_input("Cidade", value=produtor_data["cidade"])
                    estado = st.text_input(
                        "Estado (UF)", value=produtor_data["estado"], max_chars=2
                    )
                    area_total = st.number_input(
                        "Área Total (ha)",
                        min_value=0.0,
                        value=produtor_data["area_total"],
                        step=0.01,
                    )
                    area_agricultavel = st.number_input(
                        "Área Agricultável (ha)",
                        min_value=0.0,
                        value=produtor_data["area_agricultavel"],
                        step=0.01,
                    )
                    area_vegetacao = st.number_input(
                        "Área de Vegetação (ha)",
                        min_value=0.0,
                        value=produtor_data["area_vegetacao"],
                        step=0.01,
                    )
                    culturas = st.multiselect(
                        "Culturas Plantadas",
                        ["Soja", "Milho", "Algodão", "Café", "Cana de Açúcar"],
                        default=produtor_data["culturas_plantadas"],
                    )

                    submit_button = st.form_submit_button("Atualizar Produtor")

                    if submit_button:

                        if area_agricultavel + area_vegetacao > area_total:
                            st.error(
                                "A soma das áreas agricultável e vegetação não pode ser maior que a área total."
                            )
                        else:
                            updated_data = {
                                "cpf_cnpj": cpf_cnpj,
                                "nome_produtor": nome_produtor,
                                "nome_fazenda": nome_fazenda,
                                "cidade": cidade,
                                "estado": estado,
                                "area_total": area_total,
                                "area_agricultavel": area_agricultavel,
                                "area_vegetacao": area_vegetacao,
                                "culturas_plantadas": culturas,
                            }
                            result = update_produtor(selected_id, updated_data)
                            if isinstance(result, dict) and "detail" in result:
                                st.error(
                                    f"Erro ao atualizar produtor: {result['detail']}"
                                )
                            else:
                                st.success("Produtor atualizado com sucesso!")

    elif choice == "Deletar":
        st.subheader("Deletar Produtor")

        produtores = get_produtores()
        produtor_ids = [prod["id"] for prod in produtores]
        selected_id = st.selectbox("Selecione o Produtor", produtor_ids)

        if selected_id:
            produtor_data = next(
                (prod for prod in produtores if prod["id"] == selected_id), None
            )
            if produtor_data:
                st.write(
                    f"Tem certeza que deseja deletar o produtor **{produtor_data['nome_produtor']}**?"
                )

                if st.button("Deletar"):
                    result = delete_produtor(selected_id)
                    if isinstance(result, dict) and "detail" in result:
                        st.error(f"Erro ao deletar produtor: {result['detail']}")
                    else:
                        st.success("Produtor deletado com sucesso!")
                        st.experimental_rerun()


if __name__ == "__main__":
    main()
