import streamlit as st

from pump_calc import calculate_vial_duration


def main():
    st.set_page_config(layout="centered", page_title="Vial Duration Calculator")

    # Initialize session state for tracking changes
    if "prev_duration" not in st.session_state:
        st.session_state.prev_duration = None
    if "prev_day_consumption" not in st.session_state:
        st.session_state.prev_day_consumption = None
    if "prev_night_consumption" not in st.session_state:
        st.session_state.prev_night_consumption = None
    if "prev_boost_consumption" not in st.session_state:
        st.session_state.prev_boost_consumption = None

    # Container 1: Flow rates and vial amount
    with st.container(border=False):
        col1, col2 = st.columns(2)

        with col1:
            vial_amount = st.number_input(
                "Vial Amount (ml)", min_value=0, max_value=100, value=10.0, step=0.1
            )
            night_flow_rate = st.number_input(
                "Night Flow Rate (ml/hour)",
                min_value=0,
                max_value=10,
                value=0.27,
                step=0.01,
            )

        with col2:
            base_flow_rate = st.number_input(
                "Base Flow Rate (ml/hour)",
                min_value=0,
                max_value=10,
                value=0.44,
                step=0.01,
            )
            boost_flow_rate = st.number_input(
                "Boost Flow Rate (ml)", min_value=0, max_value=10, value=0.3, step=0.1
            )

    st.divider()

    # Container 2: Time settings and boosts
    with st.container(border=False):
        col1, col2 = st.columns(2)

        with col1:
            night_hours = st.number_input(
                "Night Rate Hours",
                value=8,
                min_value=0,
                max_value=24,
                step=1,
                help="This assumes a single night cycle per vial and might not be accurate for other scenarios.",
            )

        with col2:
            expected_boosts = st.number_input(
                "Expected Number of Boosts", min_value=0, max_value=12, value=0, step=1
            )

        # Calculate button
        if st.button(
            "Calculate Vial Duration", type="primary", use_container_width=True
        ):
            result = calculate_vial_duration(
                vial_amount,
                base_flow_rate,
                boost_flow_rate,
                night_flow_rate,
                expected_boosts,
                night_hours,
            )

            st.divider()

            # Display results
            st.subheader("Duration and Usage Estimates:")

            # Calculate deltas if previous values exist
            duration_delta = (
                None
                if st.session_state.prev_duration is None
                else result["estimated_hours"] - st.session_state.prev_duration
            )
            day_delta = (
                None
                if st.session_state.prev_day_consumption is None
                else result["day_consumption"] - st.session_state.prev_day_consumption
            )
            night_delta = (
                None
                if st.session_state.prev_night_consumption is None
                else result["night_consumption"]
                - st.session_state.prev_night_consumption
            )
            boost_delta = (
                None
                if st.session_state.prev_boost_consumption is None
                else result["boost_consumption"]
                - st.session_state.prev_boost_consumption
            )

            # Main duration metric in a container for emphasis
            with st.container(border=False):
                col1, col2 = st.columns(2, border=False)
                with col1:
                    with st.container(border=True):
                        st.metric(
                            "Vial Duration (0% remaining)",
                            f"{result['estimated_hours']:.1f} hours",
                            delta=(
                                f"{duration_delta:.1f} hours"
                                if duration_delta is not None
                                else None
                            ),
                            delta_color="off",
                            help="How long the vial is estimated to last at the current flow rates.",
                        )
                # with col2:
                #     st.metric(
                #         "Vial Duration (10% remaining)",
                #         f"{(result['estimated_hours'] * 0.9):.1f} hours",
                #         delta=(
                #             f"{(duration_delta * 0.9):.1f} hours"
                #             if duration_delta is not None
                #             else None
                #         ),
                #         delta_color="off",
                #     )
            with st.container(border=False):
                col1, col2, col3 = st.columns(3, border=True)
                with col1:
                    st.metric(
                        "Base Rate Consumption",
                        f"{result['day_consumption']:.2f} ml",
                        delta=(
                            f"{day_delta:.2f} ml" if day_delta is not None else None
                        ),
                        delta_color="off",
                        help=f"Amount used during base rate hours",
                    )
                with col2:
                    st.metric(
                        "Night Rate Consumption",
                        f"{result['night_consumption']:.2f} ml",
                        delta=(
                            f"{night_delta:.2f} ml" if night_delta is not None else None
                        ),
                        delta_color="off",
                        help=f"Amount used during night rate hours",
                    )
                with col3:
                    st.metric(
                        "Boost Consumption",
                        f"{result['boost_consumption']:.2f} ml",
                        delta=(
                            f"{boost_delta:.2f} ml" if boost_delta is not None else None
                        ),
                        delta_color="off",
                        help=f"Amount used for {expected_boosts} boosts. Boosts are treated as instantaneous events.",
                    )

            # Store current values for next comparison
            st.session_state.prev_duration = result["estimated_hours"]
            st.session_state.prev_day_consumption = result["day_consumption"]
            st.session_state.prev_night_consumption = result["night_consumption"]
            st.session_state.prev_boost_consumption = result["boost_consumption"]


if __name__ == "__main__":
    main()
