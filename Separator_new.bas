Attribute VB_Name = "Separator_new"
Sub Separator_new()

Const strStartDir = "c:\test" 'папка, с которой начать обзор файлов
Const strSaveDir = "c:\test\result" 'папка, в которую будет предложено сохранить результат
'Dim blInsertNames As Integer  'вставлять строку заголовка (книга, лист) перед содержимым листа

Dim tbl As Range
 
Dim wbTarget As New Workbook, wbSrc As Workbook, shSrc As Worksheet, shTarget As Worksheet, arFiles, _
    i As Integer, stbar As Boolean, clTarget As Range
    
Application.ScreenUpdating = False
On Error Resume Next    'если указанный путь не существует, обзор начнется с пути по умолчанию
ChDir strStartDir
On Error GoTo 0
With Application    'меньше писанины
arFiles = .GetOpenFilename("Excel Files (*.xlsx), *.xlsx", , "Объединить файлы", , True)
If Not IsArray(arFiles) Then End 'если не выбрано ни одного файла
Set wbTarget = Workbooks.Add(template:=xlWorksheet)
Set shTarget = wbTarget.Sheets(1)
    .ScreenUpdating = False
    stbar = .DisplayStatusBar
    .DisplayStatusBar = True

For i = 1 To UBound(arFiles)
    .StatusBar = "Обработка файла " & i & " из " & UBound(arFiles)
    .DisplayAlerts = False
    .EnableEvents = False
    ' .Visible = False
    Set wbSrc = Workbooks.Open(arFiles(i), CorruptLoad:=xlExtractData, ReadOnly:=True)
    For Each shSrc In wbSrc.Worksheets
        If IsNull(shSrc.UsedRange.Text) Then 'лист не пустой
            Set clTarget = shTarget.Range("A1").Offset(shTarget.Range("A1").SpecialCells(xlCellTypeLastCell).Row, 0)
            Set tbl = shSrc.UsedRange
            tbl.Offset(1, 0).Resize(tbl.Rows.Count - 1, tbl.Columns.Count).Copy clTarget
            'сдвиг таблицы на строку вниз и низ на строку вверх
        End If
    Next
    wbSrc.Close False   'закрыть без запроса на сохранение
Next
    .ScreenUpdating = True
    .DisplayStatusBar = stbar
    .StatusBar = False
 
On Error Resume Next    'если указанный путь не существует и его не удается создать,
                        'обзор начнется с последней использованной папки
If Dir(strSaveDir, vbDirectory) = Empty Then MkDir strSaveDir
ChDir strSaveDir
On Error GoTo 0
arFiles = .GetSaveAsFilename("Результат", "Excel Files (*.xlsx), *.xlsx", , "Сохранить объединенную книгу")
 
If VarType(arFiles) = vbBoolean Then 'если не выбрано имя
    GoTo save_err
Else
    On Error GoTo save_err
    wbTarget.SaveAs arFiles
End If
End
save_err:
    MsgBox "Книга не сохранена!", vbCritical
End With
Application.ScreenUpdating = True
End Sub

