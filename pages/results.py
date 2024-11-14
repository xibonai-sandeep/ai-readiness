import streamlit as st
import plotly.graph_objects as go
from openai_helper import generate_ai_readiness_score
import json


def create_radar_chart(area_scores):
    categories = list(area_scores.keys())
    values = list(area_scores.values())

    fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill="toself"))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False
    )

    return fig


def create_benchmark_chart(company_score, industry_avg, top_10, bottom_10, median):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Your Company", "Industry Average", "Top 10%", "Median", "Bottom 10%"],
            y=[company_score, industry_avg, top_10, median, bottom_10],
            marker_color=["#1E90FF", "#808080", "#90EE90", "#FFA500", "#FF6347"],
        )
    )

    fig.update_layout(
        title="AI Readiness Score Benchmark",
        yaxis_title="AI Readiness Score",
        yaxis=dict(range=[0, 100]),
    )

    return fig


def display_dict_or_list(data, indent_level=0):
    """
    A helper function to recursively display nested dictionaries or lists.
    """
    indent = "&nbsp;" * 4 * indent_level  # Adjusts for indentation in markdown

    if isinstance(data, dict):
        for key, value in data.items():
            st.markdown(f"{indent}**{key}:**", unsafe_allow_html=True)
            if isinstance(value, (dict, list)):
                display_dict_or_list(value, indent_level + 1)
            else:
                st.markdown(f"{indent}&nbsp;&nbsp;{value}", unsafe_allow_html=True)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                display_dict_or_list(item, indent_level + 1)
            else:
                st.markdown(f"{indent}- {item}", unsafe_allow_html=True)


def app():
    st.header("Assessment Results")

    if "answers" not in st.session_state or not st.session_state.answers:
        st.warning("Please complete the assessment first.")
        return

    if "ai_readiness_result" not in st.session_state:
        try:
            # Generate AI readiness score and insights
            answers_text = "\n".join(
                [
                    f"Q{i+1}: {answer}"
                    for i, answer in enumerate(st.session_state.answers.values())
                ]
            )
            ai_readiness_result = generate_ai_readiness_score(
                answers_text, st.session_state.company_info
            )
            st.session_state.ai_readiness_result = ai_readiness_result

            # Print the raw AI readiness result
            print("Raw AI Readiness Result:")
            print(json.dumps(ai_readiness_result, indent=2))

        except Exception as e:
            print(f"Exception details: {type(e).__name__}: {str(e)}")
            st.error(f"An error occurred while generating results: {str(e)}")
            st.write("Please try again or contact support if the issue persists.")
            return

    # Display results
    display_results(st.session_state.ai_readiness_result)

    # Reset button
    if "reset_button_key" not in st.session_state:
        st.session_state.reset_button_key = 0

    if st.button(
        "Start New Assessment", key=f"reset_button_{st.session_state.reset_button_key}"
    ):
        for key in ["company_info", "questions", "answers", "ai_readiness_result"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.reset_button_key += 1
        st.success(
            "Assessment reset. Please start again from the Company Information page."
        )
        st.experimental_rerun()


def display_results(ai_readiness_result):
    with st.container():
        # Overall Score
        st.markdown(
            "<h3 style='color: #1E90FF;'>AI Readiness Score</h3>",
            unsafe_allow_html=True,
        )
        overall_score = ai_readiness_result.get("overall_score", "N/A")
        st.markdown(
            f"<b>Overall Score:</b> {overall_score}/100",
            unsafe_allow_html=True,
        )
        explanation = ai_readiness_result.get(
            "explanation", "No explanation available."
        )
        st.markdown(
            f"<b>Explanation:</b> {explanation}",
            unsafe_allow_html=True,
        )

        # Area Scores
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h3 style='color: #1E90FF;'>Area Scores</h3>", unsafe_allow_html=True
        )
        area_scores = ai_readiness_result.get("area_scores", {})
        if isinstance(area_scores, dict):
            radar_chart = create_radar_chart(area_scores)
            st.plotly_chart(radar_chart)
            for area, score in area_scores.items():
                st.markdown(f"- **{area}:** {score}/100")
        else:
            st.write("No area scores available or invalid format.")

        # Strengths and Improvement Areas
        for title, key in [
            ("Strengths", "strengths"),
            ("Improvement Areas", "improvement_areas"),
        ]:
            st.markdown(
                f"<h3 style='color: #1E90FF;'>{title}</h3>", unsafe_allow_html=True
            )
            items = ai_readiness_result.get(key, [])
            if isinstance(items, list):
                for item in items:
                    st.markdown(f"- {item}")
            else:
                st.write(f"No {title.lower()} available or invalid format.")

        # Projected Score
        st.markdown(
            "<h3 style='color: #1E90FF;'>Projected Score</h3>", unsafe_allow_html=True
        )
        projected_score = ai_readiness_result.get("projected_score", "N/A")
        st.markdown(f"**Projected Score in 12 months:** {projected_score}/100")

        # Risks and Opportunities
        for title, key in [("Risks", "risks"), ("Opportunities", "opportunities")]:
            st.markdown(
                f"<h3 style='color: #1E90FF;'>{title}</h3>", unsafe_allow_html=True
            )
            items = ai_readiness_result.get(key, [])
            if isinstance(items, list):
                for item in items:
                    st.markdown(f"- {item}")
            else:
                st.write(f"No {title.lower()} available or invalid format.")

        # AI Use Cases
        st.markdown(
            "<h3 style='color: #1E90FF;'>AI Use Cases</h3>", unsafe_allow_html=True
        )
        use_cases = ai_readiness_result.get("ai_use_cases", {})
        st.markdown("**Current Use Cases:**")
        st.markdown(f"- {use_cases.get('current', 'No current use cases available.')}")
        st.markdown("**Ideal Scenarios:**")
        st.markdown(f"- {use_cases.get('ideal', 'No ideal scenarios available.')}")

        # Policy and Strategy Insights
        st.markdown(
            "<h3 style='color: #1E90FF;'>Policy and Strategy Insights</h3>",
            unsafe_allow_html=True,
        )
        policy_insights = ai_readiness_result.get(
            "policy_strategy_insights", "No policy and strategy insights available."
        )
        st.write(policy_insights)

        # Recommendations for Future
        st.markdown(
            "<h3 style='color: #1E90FF;'>Recommendations for Future</h3>",
            unsafe_allow_html=True,
        )
        recommendations = ai_readiness_result.get("recommendations_for_future", [])
        if isinstance(recommendations, list):
            for recommendation in recommendations:
                st.markdown(f"- {recommendation}")
        else:
            st.markdown("No recommendations available or invalid format.")
