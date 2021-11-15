import unittest
from flask_login import current_user
from models import User,Blog,Comment




class Test_user(unittest.TestCase):
    
    def setUp(self):
        self.new_user = User(email = 'tim@gmail.com', username = 'timo', password = '1234')
        self.new_blog = Blog(title = 'world of tech', category='technology', content='technology moves very first', user_id = self.new_user.id)
        self.new_comment = Comment(content='Good work', blog_id = self.new_blog.id, user_id = self.new_user.id)

    def tearDown(self):
        Blog.query.delete()
        User.query.delete()

    def test_password_setter(self):
    
        self.assertTrue(self.new_user.password_hash is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('1234'))
     
    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog, Blog)) 
        self.assertTrue(isinstance(self.new_comment,Comment))   
        
    def test_user(self):
        pass
    
    def test_pitch(self):
        pass
    
    def test_comment(self):
        pass