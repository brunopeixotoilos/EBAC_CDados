import streamlit as st

def intro():
    import streamlit as st

    st.write("# Exercício Streamlit - EBAC Modulo 15")
    st.sidebar.success("Selecione uma demonstração acima.")

    st.markdown(
        """
        Selecione na barra lateral a demonstração a ser visualizada.

        Todas as demonstrações foram feitas de acordo com os exemplos presentes no próprio site do _Streamlit_
    """
    )

def mapping_demo():
    import streamlit as st
    import pandas as pd
    import pydeck as pdk

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart)
to display geospatial data.
"""
    )

    @st.cache_data
    def from_data_file(filename):
        url = (
            "http://raw.githubusercontent.com/streamlit/"
            "example-data/master/hello/v1/%s" % filename
        )
        return pd.read_json(url)

    try:
        ALL_LAYERS = {
            "Bike Rentals": pdk.Layer(
                "HexagonLayer",
                data=from_data_file("bike_rental_stats.json"),
                get_position=["lon", "lat"],
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
            ),
            "Bart Stop Exits": pdk.Layer(
                "ScatterplotLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="[exits]",
                radius_scale=0.05,
            ),
            "Bart Stop Names": pdk.Layer(
                "TextLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_text="name",
                get_color=[0, 0, 0, 200],
                get_size=15,
                get_alignment_baseline="'bottom'",
            ),
            "Outbound Flow": pdk.Layer(
                "ArcLayer",
                data=from_data_file("bart_path_stats.json"),
                get_source_position=["lon", "lat"],
                get_target_position=["lon2", "lat2"],
                get_source_color=[200, 30, 0, 160],
                get_target_color=[200, 30, 0, 160],
                auto_highlight=True,
                width_scale=0.0001,
                get_width="outbound",
                width_min_pixels=3,
                width_max_pixels=30,
            ),
        }
        st.sidebar.markdown("### Map Layers")
        selected_layers = [
            layer
            for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)
        ]
        if selected_layers:
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state={
                        "latitude": 37.76,
                        "longitude": -122.4,
                        "zoom": 11,
                        "pitch": 50,
                    },
                    layers=selected_layers,
                )
            )
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

def plotting_demo():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!
"""
    )

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


def data_frame_demo():
    import streamlit as st
    import pandas as pd
    import altair as alt

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
    st.write(
        """
        This demo shows how to use `st.write` to visualize Pandas DataFrames.

(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)
"""
    )

    @st.cache_data
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )
            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

def uber_pickups_ny():
    import streamlit as st
    import pandas as pd
    import numpy as np

    st.title('Uber pickups in NYC')

    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
                'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

    @st.cache_data
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data

    data_load_state = st.text('Loading data...')
    data = load_data(10000)
    data_load_state.text("Done! (using st.cache_data)")

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    st.subheader('Number of pickups by hour')
    hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
    st.bar_chart(hist_values)

    # Some number in the range 0-23
    hour_to_filter = st.slider('hour', 0, 23, 17)
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

    st.subheader('Map of all pickups at %s:00' % hour_to_filter)
    st.map(filtered_data)

def ex_sinasc():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os
    import sys
    import streamlit as st

    sns.set_theme()

    def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
        # Cria uma nova figura
        fig, ax = plt.subplots(figsize=[15, 5])

        if opcao == 'nada':
            pd.pivot_table(df, values=value, index=index,
                        aggfunc=func).plot(ax=ax)
        elif opcao == 'sort':
            pd.pivot_table(df, values=value, index=index,
                        aggfunc=func).sort_values(value).plot(ax=ax)
        elif opcao == 'unstack':
            pd.pivot_table(df, values=value, index=index,
                        aggfunc=func).unstack().plot(ax=ax)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        # Renderiza o gráfico no Streamlit
        st.pyplot(fig=plt)
    
        return fig  # Retorna a figura para ser usada no salvamento

    st.write(' # Análise SINASC')

    # Carregar a base de dados completa
    sinasc = pd.read_csv('./input/SINASC_RO_2019.csv')

    # Converter coluna de data para datetime
    sinasc['DTNASC'] = pd.to_datetime(sinasc['DTNASC'])

    # Obter a data mínima e máxima
    min_data = sinasc['DTNASC'].min().date()
    max_data = sinasc['DTNASC'].max().date()

    st.sidebar.write('# Filtro de Data')
    st.sidebar.write(f"Período de dados disponíveis: {min_data} até {max_data}")

    # Input para selecionar as datas
    data_inicial = st.sidebar.date_input('Data Inicial:', value=min_data, min_value=min_data, max_value=max_data)
    data_final = st.sidebar.date_input('Data Final:', value=min_data, min_value=min_data, max_value=max_data)

    sinasc = sinasc[(sinasc['DTNASC'] <= pd.to_datetime(data_final)) & (sinasc['DTNASC'] >= pd.to_datetime(data_inicial))]


    plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'count', 'quantidade de nascimento', 'data de nascimento')

    plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae', 'data de nascimento', 'unstack')

    plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe', 'data de nascimento', 'unstack')

    plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'peso medio', 'escolaridade mae', 'sort')

    plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio', 'gestacao', 'sort')

    plota_pivot_table(sinasc, 'APGAR5', 'GESTACAO', 'mean', 'apgar5 medio', 'gestacao', 'sort')

page_names_to_funcs = {
        "—": intro,
        "Plotting Demo": plotting_demo,
        "Mapping Demo": mapping_demo,
        "DataFrame Demo": data_frame_demo,
        "Exercicio Uber NY": uber_pickups_ny,
        "Exercicio SINASC": ex_sinasc
    }

demo_name = st.sidebar.selectbox("Selecione uma demonstração", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()