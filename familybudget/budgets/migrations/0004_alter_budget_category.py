# Generated by Django 5.0.7 on 2024-07-18 10:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0003_alter_budget_category_alter_budget_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='budgets', to='budgets.budgetcategory'),
        ),
    ]
