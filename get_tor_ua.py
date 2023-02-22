#!/usr/bin/env python3

import urllib.request
import subprocess


"""

// NOTE:
//   SPOOFED_HTTP_UA_OS, LEGACY_UA_GECKO_TRAIL 
//   are set in ./toolkit/components/resistfingerprinting/nsRFPService.h

// NOTE:
//   MOZILLA_UAVERSION is set in ./build/moz.configure/init.configure
//   and ultimately it comes from .config/milestone.txt after some parsing

// NOTE:
//   the following source comes from
//   ./toolkit/components/resistfingerprinting/nsRFPService.cpp

static const char* GetSpoofedVersion() {
#ifdef ANDROID
  // Return Desktop's ESR version.
  return "102.0";
#else
  return MOZILLA_UAVERSION;
#endif
}


  const char* spoofedVersion = GetSpoofedVersion();

  // "Mozilla/5.0 (%s; rv:%d.0) Gecko/%d Firefox/%d.0"
  userAgent.AssignLiteral("Mozilla/5.0 (");

  if (isForHTTPHeader) {
    userAgent.AppendLiteral(SPOOFED_HTTP_UA_OS);
  } else {
    userAgent.AppendLiteral(SPOOFED_UA_OS);
  }

  userAgent.AppendLiteral("; rv:");
  userAgent.Append(spoofedVersion);
  userAgent.AppendLiteral(") Gecko/");

#if defined(ANDROID)
  userAgent.Append(spoofedVersion);
#else
  userAgent.AppendLiteral(LEGACY_UA_GECKO_TRAIL);
#endif

  userAgent.AppendLiteral(" Firefox/");
  userAgent.Append(spoofedVersion);

"""


hdrs = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0',
  'Accept-Encoding': 'gzip, deflate, br'
}

url_base = 'https://gitlab.torproject.org/tpo/applications/tor-browser'
git_url = url_base + '.git'
branch = subprocess.check_output(["git", "ls-remote", "--symref", git_url, "HEAD"]).decode().splitlines()[0].split("\t")[0].split("/")[-1]

# this logic comes from ./build/moz.configure/init.configure
milestone_url = url_base + '/-/raw/' + branch + '/config/milestone.txt'
with urllib.request.urlopen(urllib.request.Request(method='GET', url=milestone_url, headers=hdrs)) as response:
  spoofed_version = response.readlines()[-1].decode().rstrip().split(".")[0]

rfph_url = url_base + '/-/raw/' + branch + '/toolkit/components/resistfingerprinting/nsRFPService.h'
with urllib.request.urlopen(urllib.request.Request(method='GET', url=rfph_url, headers=hdrs)) as response:
  rfph_raw = response.read()
  spoofed_ua_os = [ l for l in rfph_raw.decode().splitlines() if 'SPOOFED_HTTP_UA_OS' in l][1].split('"')[1]
  gecko_trail = [ l for l in rfph_raw.decode().splitlines() if '#define LEGACY_UA_GECKO_TRAIL' in l][0].split('"')[1]

# Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0

print("Mozilla/5.0 (%s; rv:%d.0) Gecko/%d Firefox/%d.0" % (spoofed_ua_os, int(spoofed_version), int(gecko_trail), int(spoofed_version)))


