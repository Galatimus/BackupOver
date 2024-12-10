Attribute VB_Name = "Del_SubStr2"
Sub Del_SubStr2()
    Dim sSubStr As String 'искомое слово или фраза(может быть указанием на ячейку)
    Dim lCol As Long 'номер столбца с просматриваемыми значениями
    Dim lLastRow As Long, li As Long
    Dim lMet As Long
    Dim arr
 
    sSubStr = "" 'InputBox("Укажите значение, которое необходимо найти в строке", "Запрос параметра", "")
    If sSubStr = "" Then lMet = 0 Else lMet = 1
    lCol = Val(InputBox("Укажите номер столбца, в котором искать указанное значение", "Запрос параметра", 1))
    If lCol = 0 Then Exit Sub
 
    lLastRow = ActiveSheet.UsedRange.Row - 1 + ActiveSheet.UsedRange.Rows.Count
    arr = Cells(1, lCol).Resize(lLastRow).Value
    Application.ScreenUpdating = 0
    Dim rr As Range
    For li = 1 To lLastRow
    Application.StatusBar = "Обработка строки " & li & " из " & lLastRow
        If -(InStr(arr(li, 1), sSubStr) > 0) = lMet Then
            If rr Is Nothing Then
                Set rr = Cells(li, 1)
            Else
                Set rr = Union(rr, Cells(li, 1))
            End If
        End If
    Next li
    If Not rr Is Nothing Then rr.EntireRow.Delete
    Application.ScreenUpdating = 1
	MsgBox "ГОТОВО...!"
End Sub
