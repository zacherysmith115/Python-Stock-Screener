#   P y t h o n - S t o c k - S c r e e n e r  
  
 T h e   p y t h o n   s t o c k   s c r e e n e r   i s   a   f l a s k   b a s e d   w e b   a p p l i c a t i o n   t o   h e l p   i d e n t i f y   t h e   p e r f o r m a n c e   o f   d i f f e r e n t   s e c u r i t i e s   t h a t   a r e   i n c l u d e d   i n   t h e   S & P   5 0 0   b a s e d   o n   t h e r e   G I C S   S e c t o r ,   a n d   G I C S   S u b - I n d u s t r y .   T h e   a p p l i c a t i o n   u s e s   a   S Q L A l c h e m y   d a t a b a s e   t o   s t o r e   t h e   r e l a t i o n s h i p s   o f   s e c u r i t i e s   t o   t h e r e   r e s p e c t i v e   s e c t o r   a n d   i n d u s t r y ,   a s   w e l l   a s   h i s t o r i c   d a t a   f r o m   t h e   p a s t   5   y e a r s .   A l l   d a t a   i s   p r o v i d e d   u s i n g   t h e   p y t h o n   ` y f i n a n c e `   l i b r a r y ,   a n d   i s   m a n i p u l a t e d   u s i n g   t h e   ` p a n d a s `   l i b r a r y .    
  
  
  
 # # # #   S e t u p   a n d   r u n t i m e :  
  
 T o   c r e a t e   a n   i n s t a n c e   o f   t h e   d a t a b a s e   y o u   w i l l   n e e d   r u n   t h e   ` b u i l d d b . p y `   f i l e ,   t h i s   w i l l   c r e a t e   a n   i n s t a n c e   o f   t h e   d a t a b a s e   a s   w e l l   a s   u p d a t e   i t   w i t h   a l l   t h e   n e e d e d   d a t a   f o r   t h e   a p p l i c a t i o n .   I t   d o e s   t a k e   a   f e w   m i n u t e s   t o   c o m p l e t e ,   a n d   s h o u l d   s e e   a   s i m i l a r   u p d a t e   a s   b e l o w   t o   m o n i t o r   t h e   p r o c e s s .    
  
 ` ` ` s h e l l  
 C : \ . . . \ P y t h o n - S t o c k - S c r e e n e r >   p y t h o n   . \ b u i l d d b . p y  
 C r e a t i n g   m o d e l s   a n d   r e l a t i o n s h i p s :     [ ?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%]   1 0 0 . 0 %  
 E l a p s e d   t i m e :               7 . 4 3   s  
 F e t c h i n g   h i s t o r i c   d a t a :     [ ?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%?%]   1 0 0 . 0 %  
 E l a p s e d   t i m e :             1 7 0 . 9   s  
 ` ` `  
  
  
  
 A f t e r   t h e   d a t a b a s e   i s   c r e a t e d   y o u   c a n   s i m p l y   r u n   t h e   w e b   a p p l i c a t i o n   a s   s h o w n   b e l o w .   C l i c k   t h e   U R L   t o   o p e n   i n   t h e   b r o w s e r .    
  
 ` ` ` s h e l l  
 C : \ . . . \ P y t h o n - S t o c k - S c r e e n e r >   p y t h o n   . \ a p p . p y  
   *   S e r v i n g   F l a s k   a p p   ' S c r e e n e r '   ( l a z y   l o a d i n g )  
   *   E n v i r o n m e n t :   p r o d u c t i o n  
       W A R N I N G :   T h i s   i s   a   d e v e l o p m e n t   s e r v e r .   D o   n o t   u s e   i t   i n   a   p r o d u c t i o n   d e p l o y m e n t .  
       U s e   a   p r o d u c t i o n   W S G I   s e r v e r   i n s t e a d .  
   *   D e b u g   m o d e :   o n  
   *   R e s t a r t i n g   w i t h   s t a t  
   *   D e b u g g e r   i s   a c t i v e !  
   *   D e b u g g e r   P I N :   1 6 8 - 4 4 7 - 8 9 4  
   *   R u n n i n g   o n   h t t p : / / 1 2 7 . 0 . 0 . 1 : 5 0 0 0 /   ( P r e s s   C T R L + C   t o   q u i t )  
 ` ` `  
  
 