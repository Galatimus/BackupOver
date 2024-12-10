Attribute VB_Name = "Separator_new"
Sub Separator_new()

Const strStartDir = "c:\test" '�����, � ������� ������ ����� ������
Const strSaveDir = "c:\test\result" '�����, � ������� ����� ���������� ��������� ���������
'Dim blInsertNames As Integer  '��������� ������ ��������� (�����, ����) ����� ���������� �����

Dim tbl As Range
 
Dim wbTarget As New Workbook, wbSrc As Workbook, shSrc As Worksheet, shTarget As Worksheet, arFiles, _
    i As Integer, stbar As Boolean, clTarget As Range
    
Application.ScreenUpdating = False
On Error Resume Next    '���� ��������� ���� �� ����������, ����� �������� � ���� �� ���������
ChDir strStartDir
On Error GoTo 0
With Application    '������ ��������
arFiles = .GetOpenFilename("Excel Files (*.xlsx), *.xlsx", , "���������� �����", , True)
If Not IsArray(arFiles) Then End '���� �� ������� �� ������ �����
Set wbTarget = Workbooks.Add(template:=xlWorksheet)
Set shTarget = wbTarget.Sheets(1)
    .ScreenUpdating = False
    stbar = .DisplayStatusBar
    .DisplayStatusBar = True

For i = 1 To UBound(arFiles)
    .StatusBar = "��������� ����� " & i & " �� " & UBound(arFiles)
    .DisplayAlerts = False
    .EnableEvents = False
    ' .Visible = False
    Set wbSrc = Workbooks.Open(arFiles(i), CorruptLoad:=xlExtractData, ReadOnly:=True)
    For Each shSrc In wbSrc.Worksheets
        If IsNull(shSrc.UsedRange.Text) Then '���� �� ������
            Set clTarget = shTarget.Range("A1").Offset(shTarget.Range("A1").SpecialCells(xlCellTypeLastCell).Row, 0)
            Set tbl = shSrc.UsedRange
            tbl.Offset(1, 0).Resize(tbl.Rows.Count - 1, tbl.Columns.Count).Copy clTarget
            '����� ������� �� ������ ���� � ��� �� ������ �����
        End If
    Next
    wbSrc.Close False   '������� ��� ������� �� ����������
Next
    .ScreenUpdating = True
    .DisplayStatusBar = stbar
    .StatusBar = False
 
On Error Resume Next    '���� ��������� ���� �� ���������� � ��� �� ������� �������,
                        '����� �������� � ��������� �������������� �����
If Dir(strSaveDir, vbDirectory) = Empty Then MkDir strSaveDir
ChDir strSaveDir
On Error GoTo 0
arFiles = .GetSaveAsFilename("���������", "Excel Files (*.xlsx), *.xlsx", , "��������� ������������ �����")
 
If VarType(arFiles) = vbBoolean Then '���� �� ������� ���
    GoTo save_err
Else
    On Error GoTo save_err
    wbTarget.SaveAs arFiles
End If
End
save_err:
    MsgBox "����� �� ���������!", vbCritical
End With
Application.ScreenUpdating = True
End Sub

