from enum import Enum


class PostUpdateType(Enum):
    LIKED = "liked"
    COMMENTED = "commented"
    SHARED = "shared"
