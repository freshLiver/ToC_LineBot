from nhlib.nhCommand import *
from nhlib.nhBook import *
from nhlib.nhGallery import *


class NhEyes :
    __is_healthy_mode = True
    
    
    def __init__ ( self ) :
        self.__states: [NhCommand]
        self.__states = [NhCommand.HOME]  # start at home state
        self.__galleries: [NhGallery]
        self.__galleries = list( )
        self.__reading = NhBook( )
    
    
    # *********************************************************
    # ******************* gallery conversion ******************
    # *********************************************************
    
    @staticmethod
    def galleries_to_reply_form ( galleries: list ) -> (bool, str) :
        # no gallery found
        if galleries.__len__( ) == 0 :
            return (False, "")
        
        # not empty result, convert galleries info to reply form
        reply = ""
        
        # append each gallery info in galleries to reply
        gallery: NhGallery
        for index, gallery in enumerate( galleries ) :
            reply += gallery.get_reply_form( index = index )
        
        # return all galleries' info as reply message
        return (True, reply)
    
    
    # ********************************************************
    # ********************** set status **********************
    # ********************************************************
    
    def add_galleries ( self, galleries: [NhGallery] ) :
        # convert every raw gallery info to NhGallery
        for gallery in galleries :
            # append to galleries list
            self.__galleries.append( gallery )
    
    
    def push_state ( self, state: NhCommand ) :
        self.__states.append( state )
    
    
    def open_this_gallery ( self, gallery_index: int ) :
        gallery = self.__galleries[gallery_index]
        self.__reading.set_this_gallery( gallery.link )
    
    
    def get_reading_gallery_info ( self ) -> str :
        return self.__reading.book_info_to_reply( )
    
    
    @classmethod
    def toggle_mode ( cls ) -> bool :
        cls.__is_healthy_mode = not cls.__is_healthy_mode
        return cls.__is_healthy_mode
    
    @classmethod
    def get_mode (cls) -> bool:
        return cls.__is_healthy_mode
    
    # *********************************************************
    # *********************** get status **********************
    # *********************************************************
    
    def get_current_state ( self ) -> NhCommand :
        # return last state in states (stack::top)
        return self.__states[len( self.__states ) - 1]
    
    
    def get_gallery_by_index ( self, index: int ) -> (bool, list) :
        # check if target gallery index out of range
        if 0 <= index < len( self.__galleries ) :
            return (True, self.__galleries[index])
        # if gallery index out of range, return false and empty list
        else :
            return (False, list( ))
    
    
    def get_reading_page_link ( self, page: int ) -> (bool, str) :
        # check if target page over current reading book's total pages
        if 0 <= page < self.__reading.get_total_pages( ) :
            # get target page's image link
            link = self.__reading.get_link_of_page( page )
            return (True, link)
        # page out of range
        else :
            return (False, "Target Page Out Of Range")
    
    
    # *********************************************************
    # ********************** clear status *********************
    # *********************************************************
    
    def pop_state ( self ) :
        self.__states.pop( )
    
    
    def clear_state ( self ) :
        self.__states = [NhCommand.HOME]
    
    
    def clear_galleries ( self ) :
        self.__galleries.clear( )
    
    
    def clear_reading ( self ) :
        self.__reading.close_this_book( )