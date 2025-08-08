"""initial tables

Revision ID: 0001_initial
Revises: 
Create Date: 2024-06-13
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'quizzes',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True)
    )
    op.create_index('ix_quizzes_tenant_id', 'quizzes', ['tenant_id'])
    op.create_index('ix_quizzes_title', 'quizzes', ['title'])

    op.create_table(
        'questions',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('question_type', sa.String(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('quiz_id', sa.Integer(), sa.ForeignKey('quizzes.id'))
    )

    op.create_table(
        'options',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('price_impact', sa.Float(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), sa.ForeignKey('questions.id'))
    )

    op.create_table(
        'leads',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('quiz_id', sa.Integer(), nullable=False),
        sa.Column('client_email', sa.String(), nullable=False),
        sa.Column('final_price', sa.Float(), nullable=False),
        sa.Column('answers_details', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_index('ix_leads_tenant_id', 'leads', ['tenant_id'])
    op.create_index('ix_leads_client_email', 'leads', ['client_email'])

def downgrade() -> None:
    op.drop_index('ix_leads_client_email', table_name='leads')
    op.drop_index('ix_leads_tenant_id', table_name='leads')
    op.drop_table('leads')
    op.drop_table('options')
    op.drop_table('questions')
    op.drop_index('ix_quizzes_title', table_name='quizzes')
    op.drop_index('ix_quizzes_tenant_id', table_name='quizzes')
    op.drop_table('quizzes')
