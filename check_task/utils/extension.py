def check_extension(uploaded_file, form):
    if not uploaded_file.name.endswith('.py'):
        form.add_error('file', 'Загружаемый файл должен иметь расширение .py')

