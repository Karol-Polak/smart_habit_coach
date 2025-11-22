import streamlit as st
from api_client import get_habits, create_habit, create_habit_log, get_habit_stats, get_logs_for_habit, predict_habit_probability, train_habit_model, delete_habit, update_habit
from datetime import date
import requests
from pathlib import Path
import pandas as pd

# UI

st.set_page_config(
    page_title="Smart Habit Coach",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_css():
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        with open(css_path) as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css()

st.title("🧠 Smart Habit Coach")
st.caption("Aplikacja do monitorowania nawyków")

# Sidebar
page = st.sidebar.radio(
    "Nawigacja",
    [
        "🏠 Dashboard",
        "📋 Lista nawyków",
        "➕ Dodaj nawyk",
        "✅ Zaloguj wykonanie",
        "📊 Statystyki nawyku",
    ],
)

# Ładujemy listę nawyków
habits = []
try:
    habits = get_habits()
except requests.ConnectionError:
    st.error("Nie udało się połączyć z backendem. Upewnij się, że FastAPI działa na :8000.")
except Exception as e:
    st.error(f"Wystąpił błąd podczas pobierania nawyków: {e}")


# Lista nawyków

if page == "📋 Lista nawyków":
    st.header("📋 Twoje nawyki")

    if not habits:
        st.info("Nie masz jeszcze żadnych nawyków. Dodaj pierwszy w zakładce „Dodaj nawyk”.")
    else:
        for habit in habits:
            with st.container():
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.subheader(habit["name"])
                    st.write(habit.get("description") or "_Brak opisu_")

                    with st.expander("✏️ Edytuj nawyk"):
                        new_name = st.text_input(
                            "Nazwa",
                            value=habit["name"],
                            key=f"name_{habit['id']}",
                        )
                        new_desc = st.text_area(
                            "Opis",
                            value=habit.get("description") or "",
                            key=f"desc_{habit['id']}",
                        )
                        if st.button("Zapisz zmiany", key=f"save_{habit['id']}"):
                            try:
                                update_habit(habit["id"], new_name, new_desc)
                                st.success("Zaktualizowano nawyk.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Nie udało się zaktualizować nawyku: {e}")


                with col2:
                    if st.button("🗑 Usuń", key=f"delete_{habit['id']}"):
                        try:
                            delete_habit(habit["id"])
                            st.success(f"Usunięto nawyk „{habit['name']}”")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Nie udało się usunąć nawyku: {e}")

                st.markdown("---")



# dodaj nawyk

elif page == "➕ Dodaj nawyk":
    st.header("➕ Dodaj nowy nawyk")

    with st.form("add_habit_form"):
        name = st.text_input("Nazwa nawyku", placeholder="Np. Nauka Pythona 30 min")
        description = st.text_area("Opis (opcjonalnie)")
        submitted = st.form_submit_button("Zapisz nawyk")

    if submitted:
        if not name.strip():
            st.error("Nazwa nawyku nie może być pusta.")
        else:
            try:
                habit = create_habit(name=name.strip(), description=description.strip())
                st.success(f"Nawyk utworzony! ID: {habit['id']}")
                #st.rerun()
            except Exception as e:
                st.error(f"Nie udało się utworzyć nawyku: {e}")


# zaloguj wykonanie

elif page == "✅ Zaloguj wykonanie":
    st.header("✅ Zaloguj wykonanie nawyku")

    if not habits:
        st.info("Najpierw dodaj jakiś nawyk w zakładce „Dodaj nawyk”.")
    else:
        habit_options = {f"{h['name']} (ID: {h['id']})": h["id"] for h in habits}
        habit_label = st.selectbox("Wybierz nawyk", list(habit_options.keys()))
        selected_habit_id = habit_options[habit_label]

        with st.form("log_habit_form"):
            log_date = st.date_input("Data", value=date.today())
            done = st.checkbox("Wykonano?", value=True)
            mood = st.slider("Nastrój (1-5, opcjonalnie)", 1, 5, 3)
            use_mood = st.checkbox("Zapisz nastrój", value=True)
            energy = st.slider("Poziom energii (1-5, opcjonalnie)", 1, 5, 3)
            use_energy = st.checkbox("Zapisz poziom energii", value=True)
            note = st.text_area("Notatka (opcjonalnie)")
            submitted = st.form_submit_button("Zapisz log")

        if submitted:
            try:
                saved_log = create_habit_log(
                    habit_id=selected_habit_id,
                    log_date=log_date,
                    done=done,
                    mood=mood if use_mood else None,
                    energy_level=energy if use_energy else None,
                    note=note.strip() if note.strip() else None,
                )
                st.success(
                    f"Zapisano log (ID: {saved_log['id']}) dla nawyku ID {selected_habit_id} "
                    f"na dzień {saved_log['date']}."
                )
            except Exception as e:
                st.error(f"Nie udało się zapisać loga: {e}")


if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")

    if not habits:
        st.info("Nie masz jeszcze żadnych nawyków. Zacznij od dodania pierwszego.")
    else:
        total_habits = len(habits)

        total_logs = 0
        total_done = 0
        longest_streak = 0

        for h in habits:
            stats = get_habit_stats(h["id"])
            total_logs += stats["total"]
            total_done += stats["done"]
            if stats["streak_longest"] > longest_streak:
                longest_streak = stats["streak_longest"]

        avg_success = (total_done / total_logs) if total_logs > 0 else 0.0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Liczba nawyków", total_habits)
        with col2:
            st.metric("Średnia skuteczność", f"{int(avg_success * 100)}%")
        with col3:
            st.metric("Najdłuższy streak", f"{longest_streak} dni")

        st.markdown("---")

        # wybór nawyku do szczegółowego podglądu
        habit_map = {f"{h['name']} (ID: {h['id']})": h["id"] for h in habits}
        habit_label_dash = st.selectbox(
            "Wybierz nawyk do szczegółowego podglądu",
            list(habit_map.keys()),
        )
        habit_id_dash = habit_map[habit_label_dash]

        try:
            logs = get_logs_for_habit(habit_id_dash)
            if logs:
                st.subheader(f"Ostatnie logi – {habit_label_dash}")
                df_logs = pd.DataFrame(logs)
                df_logs["date"] = pd.to_datetime(df_logs["date"])
                df_logs = df_logs.sort_values("date")

                st.dataframe(
                    df_logs[["date", "done", "mood", "energy_level", "note"]].tail(10),
                    use_container_width=True,
                )

                st.subheader("Wykonania w czasie")
                done_series = df_logs.set_index("date")["done"].astype(int)
                st.line_chart(done_series)
            else:
                st.info("Brak logów dla wybranego nawyku.")
        except Exception as e:
            st.error(f"Nie udało się pobrać logów: {e}")

# statystyki nawyku

elif page == "📊 Statystyki nawyku":
    st.header("📊 Statystyki nawyku")

    if not habits:
        st.info("Najpierw dodaj jakiś nawyk w zakładce „Dodaj nawyk”.")
    else:
        habit_options = {f"{h['name']} (ID: {h['id']})": h["id"] for h in habits}
        habit_label = st.selectbox("Wybierz nawyk", list(habit_options.keys()))
        selected_habit_id = habit_options[habit_label]

        # statystyki historyczne
        if st.button("Pobierz statystyki historyczne"):
            try:
                stats = get_habit_stats(selected_habit_id)
                st.subheader(f"Statystyki dla: {habit_label}")

                st.write(f"🔢 Łączna liczba logów: **{stats['total']}**")
                st.write(f"✅ Wykonane: **{stats['done']}**")
                st.write(f"❌ Niewykonane: **{stats['not_done']}**")
                st.write(f"📈 Skuteczność: **{int(stats['success_rate'] * 100)}%**")
                st.write(f"🔥 Aktualny streak: **{stats['streak_current']}** dni")
                st.write(f"🏆 Najdłuższy streak: **{stats['streak_longest']}** dni")

                if stats.get("by_weekday"):
                    st.subheader("Wykonania wg dni tygodnia (0=pon, 6=niedz)")

                with st.expander("Zobacz surowe logi"):
                    logs = get_logs_for_habit(selected_habit_id)
                    st.json(logs)

            except Exception as e:
                st.error(f"Nie udało się pobrać statystyk: {e}")

        st.markdown("---")

        # ML prognoza wykonania
        st.subheader("🤖 Prognoza wykonania nawyku")

        with st.form("prediction_form"):
            pred_date = st.date_input("Data, dla której chcesz prognozę", value=date.today())
            mood = st.slider("Zakładany nastrój (1–5, opcjonalnie)", 1, 5, 3)
            use_mood = st.checkbox("Uwzględnij nastrój", value=True)
            energy = st.slider("Zakładany poziom energii (1–5, opcjonalnie)", 1, 5, 3)
            use_energy = st.checkbox("Uwzględnij poziom energii", value=True)
            submitted_pred = st.form_submit_button("Policz prognozę")

        if submitted_pred:
            try:
                result = predict_habit_probability(
                    habit_id=selected_habit_id,
                    prediction_date=pred_date,
                    mood=mood if use_mood else None,
                    energy_level=energy if use_energy else None,
                )
                prob = result["probability_done"]  # np. 0.78
                percent = int(prob * 100)

                st.success(
                    f"Szacowana szansa wykonania nawyku **{habit_label}** "
                    f"dnia **{result['date']}** to około **{percent}%**."
                )
                st.caption(f"Model wytrenowany: {result.get('model_trained_at')}")
            except Exception as e:
                st.error(f"Nie udało się obliczyć prognozy: {e}")

        st.subheader("MODEL ML")

        st.subheader("⚙️ Model ML")

        if st.button("🔁 Przetrenuj model dla tego nawyku"):
            try:
                summary = train_habit_model(selected_habit_id)
                acc = int(summary["accuracy"] * 100)
                st.success(
                    f"Model wytrenowany ponownie (dokładność ok. {acc}%). "
                    f"Liczba próbek: {summary['n_samples']}, klasy: {summary['class_counts']}."
                )
                if summary.get("warning_few_samples"):
                    st.warning("Uwaga: mało danych – model może być mało stabilny.")
            except requests.HTTPError as e:
                # błąd z backendu: 400/404/500
                try:
                    detail = e.response.json().get("detail")
                except Exception:
                    detail = str(e)
                st.error(f"Nie udało się wytrenować modelu: {detail}")
            except Exception as e:
                st.error(f"Nie udało się wytrenować modelu: {e}")
