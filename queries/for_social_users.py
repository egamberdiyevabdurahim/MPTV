from enum import Enum

from database_config.db_settings import execute_query


class SocialEnum(Enum):
    INSTAGRAM = "Instagram"
    TIKTOK = "TikTok"
    YOUTUBE = "YouTube"


class SocialUsersModel:
    table_name = "social_users"
    def create_social_users_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id),
            social_media VARCHAR(255) NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )"""
        execute_query(query)
        return None

    def create_social_user(self, user_id, social_media):
        query = f"""
        INSERT INTO {self.table_name} (user_id, social_media)
        VALUES (%s, %s)
        RETURNING id;
        """
        result = execute_query(query, (user_id, social_media.value), fetch='return')
        return result

    def get_all_social_users_by_social_media(self, social_media):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE social_media = %s;
        """
        return execute_query(query, (social_media,), fetch='all')

    def get_all_social_users(self):
        query = f"""
        SELECT * FROM {self.table_name};
        """
        return execute_query(query, fetch='all')

    def get_socials_by_days(self, start_date, end_date, social_media):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE created_at BETWEEN %s AND %s
        AND social_media = %s;
        """
        return execute_query(query, (start_date, end_date, social_media), fetch='all')