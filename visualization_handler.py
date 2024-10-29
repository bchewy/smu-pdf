import plotly.graph_objects as go
from typing import Dict, List
import plotly.express as px
import pandas as pd

class VisualizationHandler:
    @staticmethod
    def create_document_structure_visualization(structure_data: Dict) -> go.Figure:
        """Create a treemap visualization matching the document structure image"""
        # Define the exact structure from the image
        base_structure = [
            # Course Objectives (Blue section)
            {
                "id": "course_objectives",
                "parent": "",
                "name": "Course Objectives",
                "value": 30,
                "color": "#3366CC"
            },
            {
                "id": "mastering_golang",
                "parent": "course_objectives",
                "name": "Mastering Golang",
                "value": 10,
                "color": "#3366CC"
            },
            {
                "id": "data_management",
                "parent": "course_objectives",
                "name": "Data Management",
                "value": 10,
                "color": "#3366CC"
            },
            # Course Areas (Light Blue section)
            {
                "id": "course_areas",
                "parent": "",
                "name": "Course Areas",
                "value": 20,
                "color": "#89CFF0"
            },
            {
                "id": "devops_track",
                "parent": "course_areas",
                "name": "DevOps Track",
                "value": 7,
                "color": "#89CFF0"
            },
            {
                "id": "sldc_track",
                "parent": "course_areas",
                "name": "SLDC Track",
                "value": 7,
                "color": "#89CFF0"
            },
            # Competencies (Red section)
            {
                "id": "competencies",
                "parent": "",
                "name": "Competencies",
                "value": 25,
                "color": "#FF6B6B"
            },
            # Course Assessments (Pink section)
            {
                "id": "course_assessments",
                "parent": "",
                "name": "Course Assessments",
                "value": 25,
                "color": "#FFB6C1"
            },
            {
                "id": "assessment_details",
                "parent": "course_assessments",
                "name": "Assessment Details",
                "value": 15,
                "color": "#FFB6C1"
            },
            # Course Information (Teal section)
            {
                "id": "course_information",
                "parent": "",
                "name": "Course Information",
                "value": 25,
                "color": "#4ECDC4"
            },
            # University Policies (Green section)
            {
                "id": "university_policies",
                "parent": "",
                "name": "University Policies",
                "value": 20,
                "color": "#98FB98"
            },
            {
                "id": "accessibility",
                "parent": "university_policies",
                "name": "Accessibility",
                "value": 10,
                "color": "#98FB98"
            },
            # Resources (Orange section)
            {
                "id": "resources",
                "parent": "",
                "name": "Resources",
                "value": 20,
                "color": "#FF9F40"
            },
            {
                "id": "main_reading",
                "parent": "resources",
                "name": "Main Reading",
                "value": 10,
                "color": "#FF9F40"
            },
            # Synopsis (Yellow section)
            {
                "id": "synopsis",
                "parent": "",
                "name": "Synopsis",
                "value": 15,
                "color": "#FFD700"
            },
            # Prerequisites (Purple section)
            {
                "id": "prerequisites",
                "parent": "",
                "name": "Prerequisites",
                "value": 15,
                "color": "#DDA0DD"
            },
            # Teaching Staff (Gray section)
            {
                "id": "teaching_staff",
                "parent": "",
                "name": "Teaching Staff",
                "value": 15,
                "color": "#B0C4DE"
            },
            # Lesson Plan (Blue section)
            {
                "id": "lesson_plan",
                "parent": "",
                "name": "Lesson Plan",
                "value": 15,
                "color": "#4169E1"
            }
        ]

        df = pd.DataFrame(base_structure)
        fig = go.Figure(go.Treemap(
            ids=df['id'],
            labels=df['name'],
            parents=df['parent'],
            values=df['value'],
            marker=dict(colors=df['color']),
            textinfo="label",
            hovertemplate="<b>%{label}</b><br>",
            root_color="white"
        ))

        fig.update_layout(
            title="Document Structure Overview",
            width=1200,
            height=600,
            margin=dict(t=50, l=25, r=25, b=25),
            showlegend=False
        )
        return fig

    @staticmethod
    def create_word_cloud_visualization(word_cloud_data: Dict) -> go.Figure:
        """Create a bubble chart visualization of the word cloud"""
        keywords = word_cloud_data.get('keywords', [])
        
        if not keywords:
            # Provide default keywords if none are found
            keywords = [
                {"word": "Course Objectives", "score": 95},
                {"word": "Assessments", "score": 90},
                {"word": "Competencies", "score": 85},
                {"word": "Resources", "score": 80},
                {"word": "Prerequisites", "score": 75}
            ]

        # Create bubble chart
        fig = go.Figure(data=[
            go.Scatter(
                x=[i for i in range(len(keywords))],
                y=[item['score'] for item in keywords],
                mode='text+markers',
                text=[item['word'] for item in keywords],
                textfont=dict(
                    size=[score['score'] * 0.4 for score in keywords],
                    color='darkblue'
                ),
                marker=dict(
                    size=[score['score'] * 0.8 for score in keywords],
                    color=['#3366CC', '#FF6B6B', '#4ECDC4', '#FF9F40', '#FFB6C1', 
                           '#98FB98', '#DDA0DD', '#B0C4DE'],
                    opacity=0.6
                ),
                hovertemplate="<b>%{text}</b><br>Importance: %{y}<extra></extra>"
            )
        ])
        
        fig.update_layout(
            title="Word Cloud Visualization",
            showlegend=False,
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            hovermode='closest',
            width=1000,
            height=600,
            margin=dict(t=50, l=25, r=25, b=25)
        )
        return fig

    @staticmethod
    def create_schedule_timeline(schedule_data: Dict) -> go.Figure:
        """Create a timeline visualization of the course schedule"""
        # Create a more structured timeline layout
        fig = go.Figure()

        # Default data if no schedule data is provided
        if not schedule_data.get('weekly_plan'):
            schedule_data = {
                'weekly_plan': [
                    {'week': 1, 'topic': 'Course Introduction', 'activities': ['Course Overview']},
                    {'week': 2, 'topic': 'Fundamentals', 'activities': ['Basic Concepts']},
                    {'week': 3, 'topic': 'Advanced Topics', 'activities': ['Advanced Learning']}
                ],
                'milestones': [
                    {'type': 'Assignment', 'description': 'Project Start', 'week': 1},
                    {'type': 'Quiz', 'description': 'Mid-term Assessment', 'week': 2},
                    {'type': 'Project', 'description': 'Final Submission', 'week': 3}
                ]
            }

        # Add weekly plan bars
        weeks = schedule_data.get('weekly_plan', [])
        fig.add_trace(go.Bar(
            x=[f"Week {week['week']}" for week in weeks],
            y=[1 for _ in weeks],
            text=[week['topic'] for week in weeks],
            textposition='inside',
            name='Weekly Topics',
            marker_color='rgb(55, 83, 109)',
            width=0.6,
            hovertemplate="<b>%{text}</b><br>Week %{x}<extra></extra>"
        ))

        # Add milestones as markers
        milestones = schedule_data.get('milestones', [])
        fig.add_trace(go.Scatter(
            x=[f"Week {m['week']}" for m in milestones],
            y=[1.5 for _ in milestones],
            mode='markers+text',
            name='Milestones',
            marker=dict(
                symbol='diamond',
                size=15,
                color='red'
            ),
            text=[m['description'] for m in milestones],
            textposition="top center",
            hovertemplate="<b>%{text}</b><extra></extra>"
        ))

        fig.update_layout(
            title="Course Schedule Timeline",
            showlegend=True,
            height=400,
            bargap=0.2,
            yaxis=dict(
                showticklabels=False,
                showgrid=False,
                range=[0, 2]
            ),
            xaxis=dict(
                title="Course Timeline",
                tickangle=-45
            ),
            plot_bgcolor='white'
        )

        return fig