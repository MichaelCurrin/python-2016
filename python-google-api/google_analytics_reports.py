# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 16:31:11 2016
Updated 21 Sept 2016

@author: michaelcurrin

Daily traffic report for website data in Google Analytics API

Required points:
		Purpose: look for sudden spikes in session volumes each day.
		Daily mail  to be sent automatically to Media dept.
		Show values for start of month to yesterday’s date.
		Run on schedule
		Split by brand and then into Channel grouping. 
         All channel names within the brand (segment) are shown 
         without any filtering or renaming. 

"""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import mikes_toolbox


# API connection methods


def authorise(service_account_email, key_file_location):
    """
    Pass account credentials details to get_service method.
    
    To find your credentials
        go to Google Analytics
        create a project 
        create a service account within that
        download .p12 file (not the JSON file)
        give the .p12 file a shorter name
        put the service account email and the .p12 name in your config file
        
    If GA accounts (e.g. insights@consulting.com) are not yours, 
        ensure the service account has been added as a user on the saccount e.g. Lumen or RCS, 
        with at least read only access. This will then apply to all sites/views/properties
        witthin that account too.

    Args
        service_account_email: service email
        key_file_location:  name of p12 file in current directory.
    Returns
        connection: authorised connection
    """

    # Define the auth scopes to request.
    scope = ["https://www.googleapis.com/auth/analytics.readonly"]

    # Authenticate and construct service.
    connection = get_service(
        "analytics", "v3", scope, key_file_location, service_account_email
    )
    return connection


def get_service(api_name, api_version, scope, key_file_location, service_account_email):
    """
    Get a service that communicates to a Google API.
    (Based on HelloAnalytics.py)

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scope: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account p12 key file.
        service_account_email: The service account email address.

    Returns:
        A service that is connected to the specified API.
    """
    credentials = ServiceAccountCredentials.from_p12_keyfile(
        service_account_email, key_file_location, scopes=scope
    )

    http = credentials.authorize(httplib2.Http())

    service = build(api_name, api_version, http=http)
    return service


# Query methods


def get_sessions_totals(
    service, profile_id, startDate, endDate, segment, metrics="ga:sessions"
):
    """
    Query the API for channel grouping for sessions WITHOUT dimensions
    
    Args:
        service: authenticated connection object
        profile_id: view in GA in the form 'ga:12345678'
        startDate: start of query as YYYY-MM-DD
        endDate: end of query as YYYY-MM-DD
        segment: Segment to apply. Leave blank if not required.
        metrics: string of comma separated values. Leave blank for default.
        
    Returns: query output
    """
    # Execute.
    # Note: must coose between query structure with and without segment
    # Since using blank value as segment = '' gives an error as
    # "Invalid value '' for segment parameter."

    if segment:
        result = (
            service.data()
            .ga()
            .get(
                ids=profile_id,
                start_date=startDate,
                end_date=endDate,
                metrics=metrics,
                segment=segment,
            )
            .execute()
        )
    else:
        result = (
            service.data()
            .ga()
            .get(
                ids=profile_id, start_date=startDate, end_date=endDate, metrics=metrics
            )
            .execute()
        )
    return result


def get_sessions_by_dimensions(
    service, profile_id, startDate, endDate, segment, dimensions, metrics="ga:sessions"
):
    """
    Query the API for channel grouping for sessions WITH dimensions
    And sort query output by the first dimension specified
    
    Args:
        service: authenticated connection object
        profile_id: view in GA in the form 'ga:12345678'
        startDate: start of query as YYYY-MM-DD
        endDate: end of query as YYYY-MM-DD
        segment: Segment to apply. Leave blank if not required.
        dimensions: string of comma separated values. 
        metrics: string of comma separated values. Leave blank for default.
        
    Returns: query output
    """
    # if there is more than one dimension,
    # use a substring for the first dimension before the 1st comma
    sort = dimensions
    if sort.find(",") > 0:
        sort = sort[: sort.find(",")]

    # Execute.
    # Choose between query structure with and without segment
    if segment:
        result = (
            service.data()
            .ga()
            .get(
                ids=profile_id,
                start_date=startDate,
                end_date=endDate,
                metrics=metrics,
                segment=segment,  # with segment
                dimensions=dimensions,
                sort=sort,
            )
            .execute()
        )
    else:
        result = (
            service.data()
            .ga()
            .get(
                ids=profile_id,
                start_date=startDate,
                end_date=endDate,
                metrics=metrics,
                dimensions=dimensions,
                sort=sort,
            )
            .execute()
        )
    return result


def GetAnalyticsData(
    client_name,
    site_data,
    segment_data,
    goal_data,
    inputDimensions,
    inputMetrics,
    service_account_email,
    key_file_location,
    startDate,
    endDate,
    countOfDays,
    dimensions_data={},
):
    """
    Connect to Google AnalyticsAPI with credentials
    Generate a series of tables for reporting on each site and its segments
    
    Args
        client_name: string. Name to print on the report
        site_data: dictionary. Pairs of site names and GA ID values.
        segment_data: dictionary. Pairs of site names and segment names, 
                        where segment names are paired with segment codes
        goal_data: dictionary. Pairs of site names and segment names,
                        where segment names are paired with goal numbers
                        in a list of main and secondary goals (if applicable)
        inputDimensions: string. Names of dimensions for GA API, split with 
                        a comma.
        inputMetrics: string. names of metrics for GA API, split with a comma.
        service_account_email: string. Email address of service account.
        key_file_location: name of p12 file containing authorisation data.
        startDate: date. Start date of the query period.
        endDate: date. End date of the query period.
        countOfDays: int. Number of days between start and end date.
        dimensions_data: dictionary. Null by default. If this has been 
                        specified, then it will be used to override the
                        inputDimensions value.
    Returns
        tableList: metadata and data as a list, with neat table formatting
        reportSummary: String. Description of report, including client name 
                    and date range.
    """

    service = authorise(service_account_email, key_file_location)

    dateTable = mikes_toolbox.formatTable(
        ("Start Date", "End Date", "Days"),
        [(startDate, endDate, countOfDays.days)],
        setBorder=False,
        setAlign="c",
    )

    reportSummary = "GA Report for %s (%s - %s)" % (
        client_name,
        startDate.strftime("%d %b"),
        endDate.strftime("%d %b"),
    )

    # List of tables for output, starting with the dates range,
    # Then followed with metadata and data for each site and segment pair
    tablesList = [dateTable]

    # Iterate through a list of sitenames using the dictionary keys
    for sitenames in site_data.keys():
        site_id = site_data[sitenames]

        # sort segments names alpabetically
        sortedSegments = sorted(segment_data[sitenames].keys())

        # process all segments within site name.
        for segmentNames in sortedSegments:

            # read segment code in GA API format
            segmentCode = segment_data[sitenames][segmentNames]

            # read the goals from the config data.
            # if there are two, use both, otherwise just the one.
            # add to the standard metrics. separate with a comma
            # use goal only if metrics are not defined

            if goal_data[sitenames][segmentNames]:

                if len(goal_data[sitenames][segmentNames]) == 1:  # single goal
                    segmentGoal = (
                        "ga:goal%sCompletions" % goal_data[sitenames][segmentNames][0]
                    )
                else:  # 2 goals
                    segmentGoal = "ga:goal%sCompletions,ga:goal%sCompletions" % (
                        goal_data[sitenames][segmentNames][0],
                        goal_data[sitenames][segmentNames][1],
                    )

                if inputMetrics:
                    metrics = inputMetrics + "," + segmentGoal
                else:
                    metrics = segmentGoal
            else:
                metrics = inputMetrics

            # Pass query metadata to PrettyTable, aligned to left
            table1 = mikes_toolbox.formatTable(
                ("Site", "Segment"),
                [(sitenames, segmentNames)],
                setBorder=False,
                setAlign="l",
            )

            # check it has been defined and override inputDimensions for
            # current query
            if dimensions_data:
                inputDimensions = dimensions_data[sitenames][segmentNames]

            # Get response from API
            APIresponse = get_sessions_by_dimensions(
                service,
                site_id,
                str(startDate),  # as YYYY-MM-DD
                str(endDate),  # as YYYY-MM-DD
                segmentCode,
                inputDimensions,
                metrics=metrics,
            )

            # Get 'name' element and remove "ga:" prefix.
            # Ignore 'columnType' and 'dataType'
            headerFormatted = map(lambda x: x["name"][3:], APIresponse["columnHeaders"])

            # Pass header and rows of API response data to PrettyTable
            if "rows" in APIresponse.keys():

                # use column total value below each metric column,
                # or null for dimensions
                totals = APIresponse["totalsForAllResults"]
                totalsRow = []
                for columns in headerFormatted:
                    if ("ga:" + columns) in totals.keys():
                        totalsRow.append(totals[("ga:" + columns)])
                    else:
                        totalsRow.append("")

                # create dividing line, fill cells to width of column header
                dividerRow = map(lambda x: "=" * len(x), headerFormatted)

                rowValues = APIresponse["rows"] + [dividerRow, totalsRow]

                table2 = mikes_toolbox.formatTable(
                    headerFormatted, rowValues, setAlign="l"
                )

            else:
                # Use a placeholder row if there are no values in table
                # repeat placeholder once for each column
                zeroDataRow = [["no data"] * len(headerFormatted)]
                table2 = mikes_toolbox.formatTable(headerFormatted, zeroDataRow)

            # Create a tuple pair  consisting of a metadata and data table.
            # Add to the output list
            tablesList.append((table1, table2))

    return tablesList, reportSummary
