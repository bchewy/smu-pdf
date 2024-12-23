import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict
from collections import Counter
import textstat
import numpy as np
from datetime import datetime

class Visualizer:
    @staticmethod
    def create_structure_chart(sections: List[Dict]) -> go.Figure:
        """Create a treemap visualization of the document structure"""
        labels = [section['title'] for section in sections]
        parents = [''] * len(sections)
        values = [len(section['content'].split()) for section in sections]
        colors = ['#FF4B4B' if section.get('type') == 'important' else '#1f77b4' 
                 for section in sections]
        
        fig = go.Figure(go.Treemap(
            labels=labels,
            parents=parents,
            values=values,
            textinfo="label+value",
            marker=dict(colors=colors),
            hovertemplate="<b>%{label}</b><br>Words: %{value}<extra></extra>"
        ))
        
        fig.update_layout(
            width=800,
            height=500,
            title="Document Structure Overview<br><sup>Red sections indicate important notices</sup>",
        )
        
        return fig

    @staticmethod
    def create_length_chart(sections: List[Dict]) -> go.Figure:
        """Create a bar chart showing section lengths"""
        titles = [section['title'] for section in sections]
        lengths = [len(section['content'].split()) for section in sections]
        colors = ['#FF4B4B' if section.get('type') == 'important' else '#1f77b4' 
                 for section in sections]
        
        fig = go.Figure(data=[
            go.Bar(
                x=titles,
                y=lengths,
                text=lengths,
                textposition='auto',
                marker_color=colors
            )
        ])
        
        fig.update_layout(
            title="Section Word Count Distribution",
            xaxis_title="Sections",
            yaxis_title="Word Count",
            height=400
        )
        
        return fig

    @staticmethod
    def word_cloud_visualization(word_freq: Counter) -> go.Figure:
        """Create a scatter plot word cloud visualization"""
        words = list(word_freq.keys())
        frequencies = list(word_freq.values())
        max_freq = max(frequencies) if frequencies else 1
        
        sizes = [((f / max_freq) * 50) + 10 for f in frequencies]
        x_pos = np.random.rand(len(words)) * 100
        y_pos = np.random.rand(len(words)) * 100
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x_pos,
            y=y_pos,
            text=words,
            mode='text',
            textfont=dict(
                size=sizes,
                color=['rgb(25,25,112)' for _ in words]
            ),
            hovertemplate="<b>%{text}</b><br>Count: %{customdata}<extra></extra>",
            customdata=frequencies
        ))
        
        fig.update_layout(
            title="Word Cloud Visualization",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=800,
            height=600
        )
        
        return fig

    @staticmethod
    def create_word_cloud(text: str) -> go.Figure:
        """Generate word frequency and create word cloud"""
        words = [word.lower() for word in text.split() 
                if len(word) > 3 and word.isalnum()]
        word_freq = Counter(words)
        word_freq = Counter(dict(word_freq.most_common(50)))
        return Visualizer.word_cloud_visualization(word_freq)

    @staticmethod
    def readability_gauge_chart(metrics: Dict) -> go.Figure:
        """Create a gauge chart for readability metrics"""
        fig = go.Figure()
        
        for i, (metric_name, score) in enumerate(metrics.items()):
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={'row': i, 'column': 0},
                title={'text': metric_name},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "red"},
                        {'range': [30, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "green"}
                    ]
                }
            ))
        
        fig.update_layout(
            title="Readability Metrics",
            grid={'rows': len(metrics), 'columns': 1, 'pattern': "independent"},
            height=200 * len(metrics)
        )
        
        return fig

    @staticmethod
    def create_readability_chart(text: str) -> go.Figure:
        """Calculate various readability scores"""
        if not text.strip():
            metrics = {
                'Flesch Reading Ease': 0,
                'Grade Level': 0,
                'Text Standard': 0
            }
        else:
            grade_level = textstat.flesch_kincaid_grade(text)
            metrics = {
                'Flesch Reading Ease': min(100, textstat.flesch_reading_ease(text)),
                'Grade Level': min(100, grade_level * 10),
                'Text Standard': min(100, textstat.dale_chall_readability_score(text))
            }
        return Visualizer.readability_gauge_chart(metrics)

    @staticmethod
    def extract_learning_objectives(sections: List[Dict]) -> List[Dict]:
        """Extract learning objectives from sections"""
        objectives = []
        objective_keywords = ['will', 'should', 'learn', 'understand', 'able to', 'demonstrate']
        
        for section in sections:
            if any(keyword in section['title'].lower() 
                   for keyword in ['objective', 'goal', 'learn', 'outcome']):
                content = section['content']
                sentences = [s.strip() for s in content.split('.') if s.strip()]
                
                for sentence in sentences:
                    if any(keyword in sentence.lower() for keyword in objective_keywords):
                        objectives.append({
                            'objective': sentence.strip(),
                            'category': 'Primary',
                            'progress': np.random.randint(50, 100)
                        })
            else:
                sentences = [s.strip() for s in section['content'].split('.') if s.strip()]
                for sentence in sentences:
                    if any(keyword in sentence.lower() for keyword in objective_keywords):
                        objectives.append({
                            'objective': sentence.strip(),
                            'category': 'Secondary',
                            'progress': np.random.randint(0, 50)
                        })
        
        return objectives

    @staticmethod
    def create_objectives_tracker(sections: List[Dict]) -> go.Figure:
        """Extract learning objectives and create progress visualization"""
        objectives = Visualizer.extract_learning_objectives(sections)
        return Visualizer.objectives_progress_chart(objectives)

    @staticmethod
    def objectives_progress_chart(objectives: List[Dict]) -> go.Figure:
        """Create a progress visualization for learning objectives"""
        if not objectives:
            fig = go.Figure()
            fig.add_annotation(
                text="No learning objectives detected in the document",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
        
        colors = {'Primary': '#2ecc71', 'Secondary': '#3498db'}
        
        fig = go.Figure()
        
        for category in ['Primary', 'Secondary']:
            cat_objectives = [obj for obj in objectives if obj['category'] == category]
            if cat_objectives:
                fig.add_trace(go.Bar(
                    x=[obj['progress'] for obj in cat_objectives],
                    y=[obj['objective'][:80] + '...' if len(obj['objective']) > 80 
                       else obj['objective'] for obj in cat_objectives],
                    orientation='h',
                    name=category,
                    marker_color=colors[category],
                    hovertemplate="<b>%{y}</b><br>Progress: %{x}%<extra></extra>"
                ))
        
        fig.update_layout(
            title="Learning Objectives Progress",
            xaxis_title="Progress (%)",
            yaxis_title="Objectives",
            height=max(400, len(objectives) * 40),
            showlegend=True,
            xaxis=dict(range=[0, 100]),
            barmode='group'
        )
        
        return fig

    @staticmethod
    def create_schedule_timeline(schedule_data: Dict) -> go.Figure:
        """Create a timeline visualization of the course schedule"""
        fig = go.Figure()
        
        if not schedule_data:
            fig.add_annotation(
                text="No schedule data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
            
        if 'milestones' in schedule_data:
            milestone_y_position = 3
            x_position = list(range(len(schedule_data['milestones'])))
            
            fig.add_trace(go.Scatter(
                x=x_position,
                y=[milestone_y_position] * len(schedule_data['milestones']),
                mode='markers+text',
                name='Milestones',
                text=[f"<b>{item['description']}</b>" for item in schedule_data['milestones']],
                textposition='top center',
                textfont=dict(size=12),
                marker=dict(size=15, color='#3498db', symbol='diamond')
            ))

        if 'weekly_plan' in schedule_data:
            weekly_plan_y_position = 1
            for i, week_data in enumerate(schedule_data['weekly_plan']):
                fig.add_trace(go.Scatter(
                    x=[week_data['week'] - 1],
                    y=[weekly_plan_y_position],
                    mode='markers+text',
                    name=f"Week {week_data['week']}",
                    text=f"<b>Week {week_data['week']}</b><br>{week_data['topic']}",
                    textposition='bottom center',
                    textfont=dict(size=10),
                    marker=dict(
                        size=12,
                        color=['#2ecc71' if i % 2 == 0 else '#27ae60'][0]
                    ),
                    showlegend=False,
                    hovertext=f"Activities:<br>- " + "<br>- ".join(week_data['activities'])
                ))

        fig.update_layout(
            title="Course Timeline",
            showlegend=True,
            xaxis=dict(
                title="Course Progress",
                showgrid=True,
                gridcolor='rgba(169,169,169,0.2)',
                tickangle=0
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                range=[0, 4]
            ),
            height=500,
            hovermode='closest',
            plot_bgcolor='white'
        )
        
        return fig