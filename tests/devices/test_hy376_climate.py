from homeassistant.components.climate import ClimateEntityFeature, HVACMode, \
  HVACAction
from homeassistant.const import PERCENTAGE, UnitOfTemperature, UnitOfTime

from custom_components.tuya_local.helpers.device_config import TuyaDeviceConfig
from tests.devices.base_device_tests import TuyaDeviceTestCase
from tests.helpers import assert_device_properties_set
from tests.mixins.climate import TargetTemperatureTests
from tests.mixins.lock import BasicLockTests
from tests.mixins.number import MultiNumberTests
from tests.mixins.select import MultiSelectTests
from tests.mixins.switch import BasicSwitchTests, MultiSwitchTests

TARGET_TEMPERATURE_DPS = "2"
CURRENT_TEMP_DPS = "3"
PRESET_MODE_DPS = "4"
CHILD_LOCK_DPS = "7"
TEMP_CALIBRATION_DPS = "44"
MIN_TEMP_DPS = "102"
MAX_TEMP_DPS = "103"
BOOST_TIME_DPS = "105"
HVACMODE_DPS = "106"
COMFORT_TEMP_DPS = "107"
ENERGY_SAVING_TEMP_DPS = "108"
VALVE_OPEN_PERCENTIGE = "109"
LOW_BATTERY_DPS = "110"
SCHEDULE_DPS = "111"
HOLIDAY_MODE_TEMP_DPS = "114"
HOLIDAY_MODE_DAYS_DPS = "117"
AUTO_UNLOCK_LOCK_DPS = "116"
WINDOW_OPEN_DETECTION_DPS = "115"

HY376_FULL_PAYLOAD = {
    TARGET_TEMPERATURE_DPS: 220,
    CURRENT_TEMP_DPS: 195,
    CHILD_LOCK_DPS: False,
    TEMP_CALIBRATION_DPS: 0,
    PRESET_MODE_DPS: "boost",
    MIN_TEMP_DPS: 1,
    MAX_TEMP_DPS: 70,
    BOOST_TIME_DPS: 900,
    SCHEDULE_DPS: "2",
    COMFORT_TEMP_DPS: 22,
    ENERGY_SAVING_TEMP_DPS: 15,
    VALVE_OPEN_PERCENTIGE: 0,
    AUTO_UNLOCK_LOCK_DPS: True,
    HVACMODE_DPS: "normal",
    "13": 0,
    LOW_BATTERY_DPS: True,
    HOLIDAY_MODE_TEMP_DPS: 15,
    WINDOW_OPEN_DETECTION_DPS: False,
    HOLIDAY_MODE_DAYS_DPS: 2,
}
HY376_MIN_PAYLOAD = {
    TARGET_TEMPERATURE_DPS: 18,
    CURRENT_TEMP_DPS: 17,
    PRESET_MODE_DPS: "BOOST",
    HVACMODE_DPS: "normal",
}

CFG_FILE = "HY367_climate.yaml"


class TestHY376Climate(
    BasicLockTests,
    TargetTemperatureTests,
    MultiSelectTests,
    MultiNumberTests,
    MultiSwitchTests,
    TuyaDeviceTestCase,
):
    __test__ = True

    def setUp(self):
        self.setUpForConfig(CFG_FILE, HY376_FULL_PAYLOAD)
        self.climate = self.entities.get("climate")
        self.setUpTargetTemperature(
            TARGET_TEMPERATURE_DPS, self.climate, min=1.0, max=70.0, step=10, scale=10
        )
        self.setUpBasicLock(CHILD_LOCK_DPS, self.entities.get("lock_child_lock"))
        self.setUpMultiSelect(
            [
                {
                    "dps": SCHEDULE_DPS,
                    "name": "select_energy_saving",
                    "options": {
                        0: "5+2",
                        1: "6+1",
                        2: "7",
                    },
                }
            ]
        )
        self.setUpMultiNumber(
            [
                {
                    "dps": BOOST_TIME_DPS,
                    "name": "number_boost_time",
                    "min": 100,
                    "max": 900,
                    "step": 100,
                    "scale": 1,
                    "unit": UnitOfTime.SECONDS,
                },
                {
                    "dps": MAX_TEMP_DPS,
                    "name": "number_maximum_temperature",
                    "category": "config",
                    "min": 15,
                    "max": 70,
                    "step": 1,
                    "scale": 1,
                    "unit": UnitOfTemperature.CELSIUS,
                },
                {
                    "dps": MIN_TEMP_DPS,
                    "name": "number_minimum_temperature",
                    "category": "config",
                    "min": 1,
                    "max": 15,
                    "step": 1,
                    "scale": 1,
                    "unit": UnitOfTemperature.CELSIUS,
                },
                {
                    "dps": COMFORT_TEMP_DPS,
                    "name": "number_comfort_temperature",
                    "category": "config",
                    "min": 10,
                    "max": 25,
                    "step": 1,
                    "scale": 1,
                    "unit": UnitOfTemperature.CELSIUS,
                },
                {
                    "dps": HOLIDAY_MODE_TEMP_DPS,
                    "name": "number_holiday_temperature",
                    "category": "config",
                    "min": 2,
                    "max": 23,
                    "step": 1,
                    "scale": 1,
                    "unit": UnitOfTemperature.CELSIUS,
                },
                {
                    "dps": TEMP_CALIBRATION_DPS,
                    "name": "number_temperature_calibration",
                    "category": "config",
                    "min": -9,
                    "max": 9,
                    "step": 1,
                    "scale": 10,
                    "unit": UnitOfTemperature.CELSIUS,
                },
                {
                    "dps": ENERGY_SAVING_TEMP_DPS,
                    "name": "number_energy_saving_temperature",
                    "category": "config",
                    "min": 2,
                    "max": 23,
                    "unit": UnitOfTemperature.CELSIUS,
                },
                {
                    "dps": HOLIDAY_MODE_DAYS_DPS,
                    "name": "number_holiday_days",
                    "category": "config",
                    "min": 1,
                    "max": 30,
                    "unit": UnitOfTime.DAYS,
                },
            ]
        )
        self.setUpMultiSwitch(
            [
                {
                    "name": "switch_open_child_lock_automatically",
                    "dps": AUTO_UNLOCK_LOCK_DPS,
                },
                {
                    "name": "switch_window_detection",
                    "dps": WINDOW_OPEN_DETECTION_DPS,
                },
            ]
        )

        self.mark_secondary(
            [
                "lock_child_lock",
                "number_maximum_temperature",
                "number_minimum_temperature",
                "number_comfort_temperature",
                "number_holiday_temperature",
                "select_energy_saving",
                "number_boost_time",
                "number_temperature_calibration",
                "number_energy_saving_temperature",
                "binary_sensor_low_battery",
                "switch_open_child_lock_automatically",
                "switch_window_detection",
                "number_holiday_days",
            ]
        )

    def test_supported_features(self):
        self.assertEqual(
            self.climate.supported_features,
            ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE,
        )

    def test_match_minimal_payload(self):
        cfg = TuyaDeviceConfig(CFG_FILE)
        self.assertTrue(cfg.matches(HY376_MIN_PAYLOAD))

    def test_hvac_mode(self):
        self.dps[HVACMODE_DPS] = "normal"
        self.assertEqual(self.climate.hvac_mode, HVACMode.AUTO)

        self.dps[HVACMODE_DPS] = "ForceOpen"
        self.assertEqual(self.climate.hvac_mode, HVACMode.HEAT)

        self.dps[HVACMODE_DPS] = "ForceClose"
        self.assertEqual(self.climate.hvac_mode, HVACMode.OFF)

    def test_target_temperature_comfort(self):
        self.dps[TARGET_TEMPERATURE_DPS] = 10
        self.dps[PRESET_MODE_DPS] = "comfort"
        self.dps[COMFORT_TEMP_DPS] = 21
        self.assertEqual(self.climate.target_temperature, 21)

    async def test_set_target_temperature_in_comfort_mode(self):
        self.dps[PRESET_MODE_DPS] = "comfort"

        async with assert_device_properties_set(
            self.climate._device, {COMFORT_TEMP_DPS: 15}
        ):
            await self.climate.async_set_target_temperature(15)

    async def test_set_target_temperature_in_eco_mode(self):
        self.dps[PRESET_MODE_DPS] = "eco"

        async with assert_device_properties_set(
            self.climate._device, {ENERGY_SAVING_TEMP_DPS: 12}
        ):
            await self.climate.async_set_target_temperature(12)

    async def test_set_target_temperature_in_away_mode(self):
        self.dps[PRESET_MODE_DPS] = "holiday"

        async with assert_device_properties_set(
            self.climate._device, {HOLIDAY_MODE_TEMP_DPS: 8}
        ):
            await self.climate.async_set_target_temperature(8)
