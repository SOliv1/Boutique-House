from django.db import migrations


def repair_catalog_columns(apps, schema_editor):
    models_to_check = (
        apps.get_model('products', 'Collection'),
        apps.get_model('products', 'Product'),
    )

    with schema_editor.connection.cursor() as cursor:
        for model in models_to_check:
            table = model._meta.db_table
            existing_columns = {
                column.name
                for column in schema_editor.connection.introspection.get_table_description(
                    cursor,
                    table,
                )
            }
            for field in model._meta.local_fields:
                if field.column not in existing_columns:
                    schema_editor.add_field(model, field)
                    existing_columns.add(field.column)


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_refresh_garden_catalog'),
    ]

    operations = [
        migrations.RunPython(
            repair_catalog_columns,
            migrations.RunPython.noop,
        ),
    ]
