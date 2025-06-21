with tab3:
    st.header("🧩 Story Activity: Sentence Ordering")
    st.markdown("📝 Select the story events in the correct order:")

    correct_order = [
        "Emma found an old compass.",
        "Emma followed the compass through the city.",
        "Emma visited an art gallery.",
        "Emma decided to become an artist."
    ]

    options = correct_order.copy()
    random.shuffle(options)

    step_keys = [f"step_{i}" for i in range(len(correct_order))]

    if 'selected_steps' not in st.session_state:
        st.session_state.selected_steps = {k: "" for k in step_keys}

    selected_steps = st.session_state.selected_steps

    def get_remaining_options(selected_steps, options, current_step):
        current_choice = selected_steps.get(current_step, "")
        chosen_elsewhere = [selected_steps[k] for k in step_keys if k != current_step and selected_steps.get(k, "") != ""]
        remaining = [opt for opt in options if (opt == current_choice) or (opt not in chosen_elsewhere)]
        return remaining

    for i, key in enumerate(step_keys):
        remaining = get_remaining_options(selected_steps, options, key)
        default_value = selected_steps.get(key, "")
        select_options = [""] + remaining
        index = 0
        if default_value in remaining:
            index = remaining.index(default_value) + 1
        selected = st.selectbox(f"Step {i+1}", select_options, index=index, key=key)
        selected_steps[key] = selected

    if st.button("Check Order"):
        user_order = [selected_steps.get(k, "") for k in step_keys]
        if "" in user_order:
            st.warning("Please select all sentences.")
        elif user_order == correct_order:
            st.success("✅ Correct order!")
        else:
            st.error("❌ Not quite! Try again.")
