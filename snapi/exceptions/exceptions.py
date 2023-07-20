# -*- coding: utf-8 -*-
# @Author: longfengpili
# @Date:   2023-07-14 16:25:45
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-20 16:12:05


# Base exception:
class SynoError(Exception):
    """Base class for an exception. Defines error_message."""

    def __init__(self, code: int, message: str):
        super().__init__(code, message)


# # Classes for when we receive an error code in the JSON from the server.
# class LoginError(SynoBaseException):
#     """Class for an error during login."""

#     def __init__(self, error_code: int):
#         self.error_code: int = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_code, error_message=ERROR_CODES[error_code])
#         else:
#             super().__init__(error_code, error_message=AUTH_ERROR_CODES[error_code])
#         return


# class DownloadStationError(SynoBaseException):
#     """Class for an error during a download station request."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code: int = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         elif error_code in DOWNLOAD_STATION_ERROR_CODES.keys():
#             super().__init__(error_message=DOWNLOAD_STATION_ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"DownloadStation Error: {error_code}", *args)
#         return


# class FileStationError(SynoBaseException):
#     """Class for an error during a file station request."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code: int = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         elif error_code in FILE_STATION_ERROR_CODES.keys():
#             super().__init__(error_message=FILE_STATION_ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"FileStation Error: {error_code}", *args)
#         return


# class VirtualizationError(SynoBaseException):
#     """Class for an error during a virtualization request."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         elif error_code in VIRTUALIZATION_ERROR_CODES.keys():
#             super().__init__(error_message=VIRTUALIZATION_ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"Virtualization Error: {error_code}", *args)
#         return


# class AudioStationError(SynoBaseException):
#     """Class for an error during an audio station request. NOTE: I can't find any documentation on the audio station
#     webAPI errors numbers and their respective messages."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"AudioStation Error: {error_code}", *args)
#         return


# class ActiveBackupError(SynoBaseException):
#     """Class for an error during ActiveBackup request. NOTE: I can't find any documentation on error codes or their
#     respective messages."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f'ActiveBackup Error: {error_code}', *args)


# class BackupError(SynoBaseException):
#     """Class for an error during backup request. NOTE: Again I can't find error code documentation."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"Backup Error: {error_code}", *args)
#         return


# class CertificateError(SynoBaseException):
#     """Class for an error during Core.Certificate request. NOTE: Lacking documentation."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code])
#         else:
#             super().__init__(error_message=f"Certificate Error: {error_code}", *args)
#         return


# class DHCPServerError(SynoBaseException):
#     """Class for an error during a DHCPServer request."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"DHCPServer Error: {error_code}", *args)
#         return


# class DirectoryServerError(SynoBaseException):
#     """Class for an error during a directory server request. NOTE: No docs on errors."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"DirectoryServer Error: {error_code}", *args)
#         return


# class DockerError(SynoBaseException):
#     """Class for an error during a docker request. NOTE: No docs on errors."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"Docker Error: {error_code}", *args)
#         return


# class DriveAdminError(SynoBaseException):
#     """Class for an error during a drive admin request. NOTE: No error docs."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"DriveAdmin Error: {error_code}", *args)
#         return


# class LogCenterError(SynoBaseException):
#     """Class for an error during a LogCenter request. NOTE: No docs on errors.... again."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"LogCenter Error: {error_code}", *args)
#         return


# class NoteStationError(SynoBaseException):
#     """Class for an error during a NoteStation request. NOTE: No error docs."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"NoteStation Error: {error_code}", *args)
#         return


# class OAUTHError(SynoBaseException):
#     """Class for an error during a OAUTH request. NOTE: No error docs."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"OAUTH Error: {error_code}", *args)
#         return


# class PhotosError(SynoBaseException):
#     """Class for an error during a Photos request. NOTE: No error docs."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"Photos Error: {error_code}", *args)
#         return


# class SecurityAdvisorError(SynoBaseException):
#     """Class for an error during a SecurityAdvisor request. NOTE: What docs?"""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"SecurityAdvisor Error: {error_code}", *args)
#         return


# class UniversalSearchError(SynoBaseException):
#     """Class for an error during UniversalSearch request. NOTE:... no docs on errors...."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"UniversalSearch Error: {error_code}", *args)
#         return


# class USBCopyError(SynoBaseException):
#     """Class for an error during a USBCopy request. NOTE: No docs on errors."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"USBCopy Error: {error_code}", *args)


# class VPNError(SynoBaseException):
#     """Class for an error during a VPN request. NOTE: No docs on errors."""

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"VPN Error: {error_code}", *args)
#         return


# class CoreSysInfoError(SynoBaseException):
#     """Class for an error during a SYNO.Core.*, 'SYNO.Backup.Service.NetworkBackup', SYNO.Storage.*,
#             'SYNO.Finder.FileIndexing.Status', 'SYNO.S2S.Server.Pair', SYNO.ResourceMonitor.*
#     """

#     def __init__(self, error_code: int, *args: object) -> None:
#         self.error_code = error_code
#         if error_code in ERROR_CODES.keys():
#             super().__init__(error_message=ERROR_CODES[error_code], *args)
#         else:
#             super().__init__(error_message=f"CoreSysInfo Error: {error_code}", *args)
#         return


# class UndefinedError(SynoBaseException):
#     """Class for undefined errors."""

#     def __init__(self, error_code: int, api_name: str, *args: object) -> None:
#         self.error_code = error_code
#         self.api_name = api_name
#         super().__init__(error_message=f"Undefined Error: API: {api_name}, Code: {error_code}", *args)
#         return
