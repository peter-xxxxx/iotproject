   M S B A M L   `   `   `  ����  SkeletonBasics-WPF8    2Microsoft.Samples.Kinect.SkeletonBasics.MainWindow   5   	   \ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    5   	   R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   -   5          � Title$  Skeleton Basics��5   	   $��768.45��6!   $��1390.5��61    � 	Resources 5         MediumGreyBrush �� Color  KinectPurpleBrush  KinectBlueBrush �� 
TargetType �� Property �� Value  SquareCheckBox �� 
TargetType �� Orientation �Name	 ��Name
 ��Name �� TextAlignment �� Triggers P� Property P� Value �� 
TargetName��%1  &	        &	 #     &	 F     '�� i     &	 �     7  7  �� 5   
   $ 	#ff6e6e6e��62   �� 5   
   $ 	#ff52318f��64   �� 5	   
   $ 	#ff00BCF2��62   �� 5
   
   " ��6   .�5      ��  �@J�SnapsToDevicePixels . 64   5      �� 5   
   " ��6   .�5      ��  � �� 5      �� 5      " ��6&   .R�5      � .+�5      �� $ 
Horizontal=�6)   
������ .+�5   "   � $ SquareCheckBoxChecked��6'   .+�5   &   �� $	 CheckedNormal��6,   $��Images\CheckedNormal.png��6C   $
��None=�6e   $��Center=�6t   �� 5   &   $	 CheckedHover��6,   $��Images\CheckedHover.png��6B   $
��None=�6c   $��Center=�6r   $y�	Collapsed=�6�   5   #   � 5   "   $ SquareCheckBoxUnchecked��6'   $y�	Collapsed=�6H   .+�5   &   �� $	 UncheckedNormal��6,   $ ��Images\UncheckedNormal.png��6E   $
��None=�6i   $��Center=�6x   �� 5   &   $	 UncheckedHover��6,   $��Images\UncheckedHover.png��6D   $
��None=�6g   $��Center=�6v   $y�	Collapsed=�6�   5   #   �� 5   "   $
 SquareCheckBoxText��6,   #��z��6H   $
 Left=�6i   $��Center=�6   8��  $��15(�6�   $��9,0,0,0q�6�   5      5       5      P� 5       �@d�	IsChecked$ falseY�6;   . �5    "   �� $ SquareCheckBoxChecked��6Q    � y�$ 	Collapsed=�6?   6Q   �� 5!   "   $ SquareCheckBoxUnchecked��6O    � y�$ Visible=�6?   6O   5"      P� 5#       �@J�IsMouseOver . . �5$   "   �� $ CheckedNormal��6Q    � y�$ 	Collapsed=�6?   6Q   �� 5%   "   $ UncheckedNormal��6Q    � y�$ 	Collapsed=�6?   6Q   �� 5&   "   $ CheckedHover��6O    � y�$ Visible=�6?   6O   �� 5'   "   $ UncheckedHover��6O    � y�$ Visible=�6?   6O   �� 5(   "   8  $ SquareCheckBoxText��6h    � ��5)      5+      5-      5.      5/      .��51      � -   5        $��
layoutGrid��51      $��10,0,0,49.2q�6   $
��Left=�62   $
��1356��6M    � RowDefinitions 52   
   �� 53      $
��Auto �6   $
��67.2��6*   �� 54      �� 55      $
��Auto �6   $��40��6*   �� 56      $
��Auto �6   $
��33.6��6*   .+�58   
   ]� $��0��6   $��
0,0,0,20.2q�6!   .+�59      �� $
��Left=�6   $��Images\Logo.png��6*   $
��Fill=�6C   $��32��6R   $��81��6^   $��0 10 0 5q�6i   �� 5:      $��Right=�6   $��0 0 -1 0q�6/   $��Bottom=�6A   #��[  6\   $��Segoe UI)�6�   $��18(�6�   Skeleton Basics6�   �� 5;      $��1��6   $��Images\Status.png��6$   $
��None=�6?   $��Center=�6N   $��0 0 0 5q�6k   5<      (� 5=   
    (� Stretch$ Uniform=�6   $��0,67,615,9.6q�6$   $��2��6:   .��5>      �� -   5        $��Image��5>      $	��523��6!   $	��338��6-    J� RenderTransformOrigin$ 0.496,0.504&�6:   $	��Top=�6^   $
��Left=�6v   5?      �� 5@   
   -   5        $��checkBoxSeatedMode��5@   �   $��2��6   #��[ 6    $��Seated Mode��6H   $��24��6^   $
��Left=�6j   $��Center=�6�   $��0,29,0,29.4q�6�   $	��130��6  �� 5A   
   -   5        $��	statusBar��5A   ?   $��3��6   $��Stretch=�6!   $��Bottom=�6P   
�������#��[  6~   $��33��6�   .@�5B      �� $��0 0 0 10q�6   $��
0,0,0,-0.2q�6/   .��5C      �� -   5        $��statusBarText��5C      $��-1 0 0 0q�61   20Click 'Seated' to change skeletal pipeline type!6u   5D      5E      �� 5F   
   -   5        $��showData��5F      $
��Left=�6"   $��23��6=   $��49,43.6,0,-33q�6I   $��3��6`    �� TextWrapping$
 Wrap=�6m   $�� ��6�   $	��Top=�6�   $	��259��6�   �� 5G   
   -   5        $
 showReceivedData��5G      $
��Left=�6/   $��788,33.8,0,0q�6J   $��1��6`   $
��Wrap=�6m   $�� ��6�   $	��Top=�6�   $	��405��6�   $	��215��6�   �� 5H   
   -	   5        $	 
ColorImage��5H      $
��Left=�6$   $	��279��6?   $��1029,33.8,0,0q�6L   $��1��6c   $	��Top=�6p   $	��317��6�   5I      5J      