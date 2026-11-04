-- The wrapper records exact playlist reloads itself.
if os.getenv('MPV_COUNT_WRAPPER') == '1' then return end

local utils = require 'mp.utils'
local options = {helper = utils.join_path(os.getenv('HOME'), 'linux-config/scripts/executable_mpv-count')}
require('mp.options').read_options(options, 'play-count')
local path, previous, native_loop

local function record()
    if not path then return end
    local result = mp.command_native({
        name = 'subprocess', playback_only = false,
        args = {'python3', options.helper, '--plain', '--record', path},
        capture_stdout = true, capture_stderr = true,
    })
    if not result or result.status ~= 0 then
        mp.msg.error('❌ Play count could not be saved; check the mpv-count helper and state-directory permissions.')
    end
end

mp.register_event('file-loaded', function()
    path, previous = nil, nil
    native_loop = mp.get_property('loop-file', 'no') ~= 'no'
    local loaded = mp.get_property('path', '')
    if loaded == '' or loaded:match('^%a[%w+.-]*://') then return end
    if loaded:sub(1, 1) ~= '/' then
        loaded = utils.join_path(mp.get_property('working-directory'), loaded)
    end
    path = loaded
    record()
end)

mp.register_event('end-file', function() path, previous = nil, nil end)
mp.observe_property('time-pos', 'number', function(_, position)
    if not path or not position then return end
    local duration = mp.get_property_number('duration')
    if native_loop and duration and duration > 0 and previous then
        local edge = math.min(1, duration * 0.9)
        -- shortcut: buffered audio can loop before time-pos reaches EOF; a manual rewind in this window also counts. Replace with a loop event if mpv adds one.
        if previous >= duration - edge and position <= edge and previous - position > math.min(0.1, duration / 10) then
            record()
        end
    end
    previous = position
end)
