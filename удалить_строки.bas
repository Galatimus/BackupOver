Attribute VB_Name = "Del_SubStr2"
Sub Del_SubStr2()
    Dim sSubStr As String '������� ����� ��� �����(����� ���� ��������� �� ������)
    Dim lCol As Long '����� ������� � ���������������� ����������
    Dim lLastRow As Long, li As Long
    Dim lMet As Long
    Dim arr
 
    sSubStr = "" 'InputBox("������� ��������, ������� ���������� ����� � ������", "������ ���������", "")
    If sSubStr = "" Then lMet = 0 Else lMet = 1
    lCol = Val(InputBox("������� ����� �������, � ������� ������ ��������� ��������", "������ ���������", 1))
    If lCol = 0 Then Exit Sub
 
    lLastRow = ActiveSheet.UsedRange.Row - 1 + ActiveSheet.UsedRange.Rows.Count
    arr = Cells(1, lCol).Resize(lLastRow).Value
    Application.ScreenUpdating = 0
    Dim rr As Range
    For li = 1 To lLastRow
    Application.StatusBar = "��������� ������ " & li & " �� " & lLastRow
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
	MsgBox "������...!"
End Sub
