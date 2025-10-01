from dataclasses import dataclass

from src.domain.shared.interfaces.instagram.version import InstagramAppVersion


@dataclass
class InstagramAppVersionInfo:
    """Информация специфичная для версии Instagram App"""

    app_version: str = "374.0.0.43.67"
    app_id: str = "567067343352427"
    version_code: str = "715888958"
    access_token: str = "567067343352427|f249176f09e26ce54212b472dbab8fa8"
    bloks_version_id: str = (
        "382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21"
    )
    capabilities: str = "3brTv10="

    module_hash: str | None = (
        "7607b7fe70423451370dd0c5de28a5be46472931dafbe414e638d872996d4304"  # Ииспользуется в https://b.i.instagram.com/api/v1/android_modules/download/
    )
    qpl_marker_id: int = 36707139


class VersionInfoRegistry:
    _version_configs: dict[InstagramAppVersion, InstagramAppVersionInfo] = {
        InstagramAppVersion.V374: InstagramAppVersionInfo(
            app_version="374.0.0.43.67",
            version_code="715888958",
            bloks_version_id="382b95cfafcbaa638772297e8d87ad1a127b8591416c5d983b8d0e68cb9b2b21",
            app_id="567067343352427",
            capabilities="3brTv10=",
        ),
    }

    @classmethod
    def get(cls, version: InstagramAppVersion) -> InstagramAppVersionInfo:
        if version not in cls._version_configs:
            raise ValueError(f"Unsupported Instagram version: {version}")
        return cls._version_configs[version]
