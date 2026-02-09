from mkpipe.spark import JdbcLoader


class PostgresLoader(JdbcLoader, variant='postgresql'):
    driver_name = 'postgresql'
    driver_jdbc = 'org.postgresql.Driver'

    def build_jdbc_url(self):
        url = (
            f'jdbc:{self.driver_name}://{self.host}:{self.port}/{self.database}'
            f'?user={self.username}&password={self.password}'
        )
        if self.schema:
            url += f'&currentSchema={self.schema}'
        return url
