from logging import Logger

import py4cytoscape as p4c
import xmltodict as xd
import requests

from server.business.models.session import Session
from server.data_access.file_system import FileSystemRepo


class Cytoscape:
    def __init__(self, logger: Logger):
        self.logger = logger

    def ping_cs(self):
        try:
            p4c.cytoscape_ping()
        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            self.logger.warning("app can’t connect to Cytoscape or Cytoscape returns an error")
            return 0
        except p4c.CyError as e:
            self.logger.error(e)
            self.logger.warning("error connecting to CyREST or version is unsupported")
            return 0

        return 1


    def apply_style(self, styles_file_path):
        self.logger.info('start applying styles')
        try:
            p4c.import_visual_styles(styles_file_path)
            data = FileSystemRepo.read(styles_file_path)
            styles_dict = xd.parse(data)
            style_name = styles_dict['vizmap']['visualStyle']['@name']
            p4c.set_visual_style(style_name)

            self.logger.info('finish applying styles')
            return style_name
        except BaseException as e:
            self.logger.error(f'apply styles: {e}')
            self.logger.warning("styles hadn't applied")
            return ''

    def apply_layout(self):
        pass

    def create_cytoscape_session(self, cys: Session) -> Session:
        p4c.import_network_from_file(cys.graph_file_path)

        if cys.styles_file_path:
            cys.styles_name = self.apply_style(cys.styles_file_path)

        if cys.session_name is None:
            cys.session_name = ''.join(cys.graph_file_path.split('.')[0:-1]) + '_session'

        cys.session_path = f'{cys.session_name}.cys'

        p4c.save_session(filename=cys.session_name)
        self.logger.info('cytoscape session file is saved')

        p4c.delete_visual_style(cys.styles_name)
        suid = p4c.get_network_suid()
        p4c.delete_network(suid)
        self.logger.info('cytoscape workspace is cleaned')

        return cys
