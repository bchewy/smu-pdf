import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict
from collections import Counter
import textstat
import numpy as np

class Visualizer:
    @staticmethod
    def create_structure_chart(sections: List[Dict]) -> go.Figure:
        """Create a treemap visualization of the document structure"""
        df = pd.DataFrame(sections)
        
        fig = go.Figure(go.Treemap(
            labels=[section['title'] for section in sections],
            parents=[''] * len(sections),
            values=[len(section['content'].split()) for section in sections],
            textinfo="label+value",
            hovertemplate="<b>%{label}</b><br>Words: %{value}<extra></extra>"
        ))
        
        fig.update_layout(
            width=800,
            height=500,
            title="Document Structure Overview",
        )
        
        return fig

    @staticmethod
    def create_length_chart(sections: List[Dict]) -> go.Figure:
        """Create a bar chart showing section lengths"""
        titles = [section['title'] for section in sections]
        lengths = [len(section['content'].split()) for section in sections]
        
        fig = go.Figure(data=[
            go.Bar(
                x=titles,
                y=lengths,
                text=lengths,
                textposition='auto',
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
        max_freq = max(frequencies)
        
        # Calculate sizes and positions
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
        # Clean and tokenize text
        words = [word.lower() for word in text.split() 
                if len(word) > 3 and word.isalnum()]
        word_freq = Counter(words)
        # Take top 50 words
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
        metrics = {
            'Flesch Reading Ease': textstat.flesch_reading_ease(text),
            'Gunning Fog': min(100, textstat.gunning_fog(text) * 10),
            'SMOG Index': min(100, textstat.smog_index(text) * 10)
        }
        return Visualizer.readability_gauge_chart(metrics)

    @staticmethod
    def extract_learning_objectives(sections: List[Dict]) -> List[Dict]:
        """Extract learning objectives from sections"""
        objectives = []
        for section in sections:
            if any(keyword in section['title'].lower() 
                  for keyword in ['objective', 'goal', 'learn', 'outcome']):
                content = section['content']
                sentences = content.split('.')
                for sentence in sentences:
                    if any(keyword in sentence.lower() 
                          for keyword in ['will', 'should', 'learn', 'understand']):
                        objectives.append({
                            'objective': sentence.strip(),
                            'progress': np.random.randint(0, 100)  # Simulated progress
                        })
        return objectives

    @staticmethod
    def objectives_progress_chart(objectives: List[Dict]) -> go.Figure:
        """Create a progress visualization for learning objectives"""
        if not objectives:
            # Create empty chart with message if no objectives found
            fig = go.Figure()
            fig.add_annotation(
                text="No learning objectives detected in the document",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
            
        fig = go.Figure(go.Bar(
            x=[obj['progress'] for obj in objectives],
            y=[obj['objective'][:100] + '...' if len(obj['objective']) > 100 
               else obj['objective'] for obj in objectives],
            orientation='h',
            marker_color='rgb(55, 83, 109)'
        ))
        
        fig.update_layout(
            title="Learning Objectives Progress",
            xaxis_title="Progress (%)",
            yaxis_title="Objectives",
            height=max(400, len(objectives) * 50),
            showlegend=False,
            xaxis=dict(range=[0, 100])
        )
        
        return fig

    @staticmethod
    def create_objectives_tracker(sections: List[Dict]) -> go.Figure:
        """Extract learning objectives and create progress visualization"""
        objectives = Visualizer.extract_learning_objectives(sections)
        return Visualizer.objectives_progress_chart(objectives)
